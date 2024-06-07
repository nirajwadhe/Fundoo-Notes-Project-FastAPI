import jwt
from datetime import datetime,timedelta
from jwt import PyJWTError
from fastapi import HTTPException
from core.setting import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def create_token(data:dict):
    if 'exp' not in data:
        data['exp']=datetime.utcnow()+timedelta(hours=1)
    encoded_jwt = jwt.encode(data,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def decode_token(encoded_jwt):    
    try : 
        decoded_jwt = jwt.decode(encoded_jwt,SECRET_KEY,ALGORITHM)
    except PyJWTError as e:
        raise HTTPException(detail="Invalid JWT Token",status_code=401)
    return decoded_jwt