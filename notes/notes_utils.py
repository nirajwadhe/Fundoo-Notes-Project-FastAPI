from fastapi import Request,HTTPException
import requests
from core.setting import settings

def auth_user(request:Request):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    response=requests.get(url=f"{settings.USER_URL}/fetchUser",params={"token":token})
    if response.status_code!=200:
        raise HTTPException(detail="User Authentication Failed",status_code=response.status_code)

    user_id=response.json().get("id")
    if user_id is None:
        raise HTTPException(status_code=401,detail="User ID not found")
    request.state.user_id=user_id