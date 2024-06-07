from fastapi import FastAPI, Depends,HTTPException
from .models import User, get_db_session
from .schema import UserRegistrationSchema,UserResponseSchema,UserLoginSchema,BaseResponseModel
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy.orm import Session
from .password_utils import get_password_hash,verify_password
from .jwt_utils import create_token,decode_token

router = FastAPI()

@router.post('/users/', response_model=UserResponseSchema,response_model_exclude={"data":["password"]})
def register_user(user_payload: UserRegistrationSchema, db: Session = Depends(get_db_session)):
    try : 
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
            email = user_payload.email,
            is_verified=False  # You might want to implement email verification later
        )
        db.add(new_user)
        db.commit()
        access_token = create_token({"sub": new_user.username})
        db.refresh(new_user)
        return {"message":"Registered Successfully",
                "status":201, 
                "data": new_user,
                "access_token":access_token}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="DataBase_Error:"+ str(e))
    
    except IndentationError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


@router.post('/login/',response_model=BaseResponseModel)
def login(user_payload: UserLoginSchema, db: Session = Depends(get_db_session)):
    try :
        user = db.query(User).filter_by(username=user_payload.username).first()
        if not user or not verify_password(user_payload.password, user.password):
            raise HTTPException(status_code=400, detail='Invalid username or password')
        return {
            "message": "Login successful",
            "status" : 200
        }
    except SQLAlchemyError as e:
        HTTPException()    