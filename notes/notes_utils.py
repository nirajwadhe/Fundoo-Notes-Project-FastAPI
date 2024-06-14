from fastapi import Request,HTTPException
import requests
from core.setting import settings
import redis,json
from datetime import datetime

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
    
class RedisManager:
    client = redis.Redis()
    
    @classmethod    
    def save(cls,payload):
        user_id = payload.get("user_id")
        note_id = payload.get("notes_id")
        # Convert datetime objects to ISO format strings
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {obj._class.name_} is not JSON serializable")   
         # Convert payload to JSON string
        payload_json = json.dumps(payload, default=convert_datetime)
        cls.client.hset(name=user_id, key=note_id, value=payload_json)
     
    @classmethod
    def read(cls, user_id):
        try:
            data = cls.client.hgetall(name=user_id)
            if data:
                return [json.loads(temp_data) for temp_data in data.values()]
            else:
                return None
        except redis.RedisError as e:
             return None
        except Exception as e:
            return None
    # this will return in list fommat

    @classmethod
    def delete(cls, user_id, note_id):
        return cls.client.hdel(user_id, note_id)    