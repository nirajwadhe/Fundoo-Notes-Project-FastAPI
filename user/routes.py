from fastapi import FastAPI, Depends,HTTPException,status
from .models import User, get_db_session
from .schema import UserRegistrationSchema,UserResponseSchema,UserLoginSchema,BaseResponseModel,UserSchema,ForgetPasswordSchema,PasswordResponseSchema,NewPasswordSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from sqlalchemy.orm import Session
from .utils import JwtUtils,PasswordUtils,EmailUtils,Audience
from core.logger_config import NOTE_LOG,logger_config
from core import create_app

router = create_app(name="user")
logger = logger_config(NOTE_LOG)

@router.post('/users/', response_model=UserResponseSchema,response_model_exclude={"data":["password"]})
def register_user(user_payload: UserRegistrationSchema, db: Session = Depends(get_db_session)):
    try : 
        logger.info("Register user attempt: %s", user_payload.username)
        existing_user = db.query(User).filter_by(username=user_payload.username).first()
        if existing_user:
            logger.warning("Username already registered: %s", user_payload.username)
            raise HTTPException(status_code=400, detail='Username already registered')
        
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
        logger.info("User registered successfully: %s", new_user.username)
        return {"message":"Registered Successfully",
                "status":201, 
                "data": new_user}
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Database error during registration: %s", str(e))
        raise HTTPException(status_code=500,detail="DataBase_Error:"+ str(e))
    
@router.post('/login/')
def login(user_payload: UserLoginSchema, db: Session = Depends(get_db_session)):
    try :
        logger.info("Login attempt: %s", user_payload.username)
        user = db.query(User).filter_by(username=user_payload.username).first()
        if not user or not PasswordUtils.verify_password(user_payload.password, user.password):
            logger.warning("Invalid login attempt: %s", user_payload.username)
            raise HTTPException(status_code=400, detail='Invalid username or password')
        
        if not user.is_verified:
            logger.warning("Unverified user login attempt: %s", user_payload.username)
            raise HTTPException(status_code=400,detail="User is Not Verified")
        
        access_token = JwtUtils.create_token({"user_id": user.id,"aud":Audience.login.value})
        logger.info("Login successful: %s", user.username)
        return {
            "message": "Login successful",
            "status" : 200,
            "access_token":access_token
        }
    except SQLAlchemyError as e:
        logger.error("Database error during login: %s", str(e))
        raise HTTPException(status_code=500,detail=str(e))    
            
@router.get('/verifyUser/')
def verify_email(token: str,db:Session=Depends(get_db_session)):
    logger.info("Email verification attempt with token: %s", token)
    payload = JwtUtils.decode_token(token=token, audience=Audience.register.value)
    userid = payload.get("user_id")
    user = db.query(User).filter(User.id == userid).first()
    if user:
        user.is_verified = True
        db.commit()   
        logger.info("User email verified: %s", user.username)
        return {"message": "User Email Verified Successfully","status":200}
    logger.warning("User not found during email verification")
    return {"message":"User Not Found","status":404}
    
@router.get("/fetchUser/",response_model=UserSchema,status_code=status.HTTP_200_OK,include_in_schema=False)
def fetch_user(token:str,db:Session=Depends(get_db_session)):
    logger.info("Fetch user attempt with token: %s", token)
    payload=JwtUtils.decode_token(token=token,audience=Audience.login.value)
    user_id=payload.get("user_id")
    user=db.query(User).where(User.id==user_id).first()
    logger.info("User fetched: %s", user.username if user else "User not found")
    return user

        
@router.post('/ForgetPassword/')
def forget_password(user_payload: ForgetPasswordSchema, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == user_payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    access_token = JwtUtils.create_token({"user_id": user.id, "aud": Audience.register.value})
    EmailUtils.send_email(user.email, subject="Password Reset", body=f"http://127.0.0.1:8000/ResetPassword/?token={access_token}")
    return {"message": "Password reset email sent successfully"}

@router.post('/ResetPassword/',response_model=BaseResponseModel)
def new_password(token:str , payload: NewPasswordSchema, db: Session = Depends(get_db_session)):
    if payload.confirm_password != payload.new_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    try:
        payload_data = JwtUtils.decode_token(token=token, audience=Audience.register.value)
        user_id = payload_data.get("user_id")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not founds")
        
        user.password = PasswordUtils.get_password_hash(payload.new_password)
        db.commit()
        db.refresh(user)
        return {"message": "Password changed successfully", "status": 200}
    
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")