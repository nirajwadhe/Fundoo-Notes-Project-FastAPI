from fastapi import FastAPI, Depends,HTTPException,status
from .models import User, get_db_session
from .schema import UserRegistrationSchema,UserResponseSchema,UserLoginSchema,BaseResponseModel,UserSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy.orm import Session
from .utils import JwtUtils,PasswordUtils,EmailUtils,Audience

router = FastAPI()

@router.post('/users/', response_model=UserResponseSchema,response_model_exclude={"data":["password"]})
def register_user(user_payload: UserRegistrationSchema, db: Session = Depends(get_db_session)):
    try : 
        # Check if the user already exists
        existing_user = db.query(User).filter_by(username=user_payload.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail='Username already registered')
        # Hash the password
        hashed_password = PasswordUtils.get_password_hash(user_payload.password)
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
        access_token = JwtUtils.create_token({"user_id": new_user.id,"aud":Audience.register.value})
        EmailUtils.send_email(new_user.email,subject="VERIFICATION EMAIL",body=f"http://127.0.0.1:8000/verifyUser?token={access_token}")
        db.refresh(new_user)
        return {"message":"Registered Successfully",
                "status":201, 
                "data": new_user}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="DataBase_Error:"+ str(e))
    
    except IndentationError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


@router.post('/login/')
def login(user_payload: UserLoginSchema, db: Session = Depends(get_db_session)):
    try :
        user = db.query(User).filter_by(username=user_payload.username).first()
        if not user or not PasswordUtils.verify_password(user_payload.password, user.password):
            raise HTTPException(status_code=400, detail='Invalid username or password')
        
        if not user.is_verified:
            raise HTTPException(status_code=400,detail="User is Not Verified")
        
        access_token = JwtUtils.create_token({"user_id": user.id,"aud":Audience.login.value})
        
        return {
            "message": "Login successful",
            "status" : 200,
            "access_token":access_token
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500,detail=str(e))    
            
@router.get('/verifyUser/')
def verify_email(token: str,db:Session=Depends(get_db_session)):
    payload = JwtUtils.decode_token(token=token, audience=Audience.register.value)
    userid = payload.get("user_id")
    user = db.query(User).filter(User.id == userid).first()
    if user:
        user.is_verified = True
        db.commit()   
        return {"message": "User Email Verified Successfully","status":200}
    return {"message":"User Not Found","status":404}
    
@router.get("/fetchUser/",response_model=UserSchema,status_code=status.HTTP_200_OK,include_in_schema=False)
def fetch_user(token:str,db:Session=Depends(get_db_session)):
    payload=JwtUtils.decode_token(token=token,audience=Audience.login.value)
    user_id=payload.get("user_id")
    user=db.query(User).where(User.id==user_id).first()
    return user