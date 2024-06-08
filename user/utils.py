import jwt
from datetime import datetime,timedelta
from jwt import PyJWTError
from fastapi import HTTPException
from core.setting import settings
from enum import Enum
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText

class Audience(Enum):
        register="register_user"
        login="login_user"
        
class JwtUtils:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    
    @staticmethod
    def create_token(data:dict):
        if 'exp' not in data:
            data['exp']=datetime.utcnow()+timedelta(hours=1)
        encoded_jwt = jwt.encode(data,JwtUtils.SECRET_KEY,algorithm=JwtUtils.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token:str,audience:str):    
        try : 
            decoded_jwt = jwt.decode(token,JwtUtils.SECRET_KEY,algorithms=[JwtUtils.ALGORITHM],audience=audience)
        except PyJWTError as e:
            raise HTTPException(detail="Invalid JWT Token",status_code=401)
        return decoded_jwt

class PasswordUtils:
    # Initialize password context for hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PasswordUtils.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordUtils.pwd_context.verify(plain_password, hashed_password)
    
class EmailUtils:

    @staticmethod
    def send_email(to_email:str, subject:str, body:str):
        try:
            msg = MIMEText(body)
            msg['From'] = settings.EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject

            with smtplib.SMTP(settings.SMTP_SERVER,settings.SMTP_PORT) as server:
                server.starttls()  # Secure the connection
                server.login(settings.EMAIL,settings.PASSWORD)
                server.sendmail(settings.EMAIL, to_email, msg.as_string())

        except Exception as e:
            print(f"Failed to send email: {e}")    