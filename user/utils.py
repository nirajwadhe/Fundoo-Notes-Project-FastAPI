import jwt
from datetime import datetime, timedelta, timezone
from jwt import PyJWTError
from fastapi import HTTPException
from core.settings import settings
from enum import Enum
from passlib.context import CryptContext

# Settings for JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

class JwtUtils:
    class Audience(str, Enum):
        REGISTER = "register_user"
        LOGIN = "login_user"

    @staticmethod
    def create_token(data: dict, audience: Audience):
        if 'exp' not in data:
            data['exp'] = datetime.now(timezone.utc) + timedelta(hours=1)
        data['aud'] = audience.value  # Set the audience
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(encoded_jwt: str, audience: Audience):
        try:
            decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM], audience=audience.value)
        except PyJWTError as e:
            raise HTTPException(status_code=401, detail="Invalid JWT Token") from e
        return decoded_jwt

class PasswordUtils:
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PasswordUtils.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordUtils.pwd_context.verify(plain_password, hashed_password)
