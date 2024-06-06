from fastapi import FastAPI, Depends,HTTPException
from .models import User, get_db_session
from .schema import UserRegistrationSchema,UserResponseSchema,UserLoginSchema
from sqlalchemy.orm import Session
from .password_utils import get_password_hash,verify_password


router = FastAPI()

@router.post('/users/', response_model=UserResponseSchema)
def register_user(user_payload: UserRegistrationSchema, db: Session = Depends(get_db_session)):
    # Check if the user already exists
    existing_user = db.query(User).filter_by(username=user_payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already registered')

    # Hash the password
    hashed_password = get_password_hash(user_payload.password)

    new_user = User(
        username=user_payload.username,
        password=hashed_password,
        first_name=user_payload.first_name,
        last_name=user_payload.last_name,
        is_verified=False  # You might want to implement email verification later
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login/')
def login(user_payload: UserLoginSchema, db: Session = Depends(get_db_session)):

    # Fetch the user from the database
    user = db.query(User).filter_by(username=user_payload.username).first()
    if not user or not verify_password(user_payload.password, user.password):
        raise HTTPException(status_code=400, detail='Invalid username or password')

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_verified": user.is_verified
        }
    }