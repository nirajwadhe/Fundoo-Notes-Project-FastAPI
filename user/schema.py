from pydantic import BaseModel, Field, ValidationError, field_validator
import re

class BaseResponseModel(BaseModel):
    message:str
    status:int
    
class UserRegistrationSchema(BaseModel):
    username: str = Field(default=" ",pattern=r"^[a-zA-Z0-9.]{3,15}$")
    password: str = Field(default=" ",min_length=8, max_length=250,description="Minimun 8 long,1 Caps, 1 Special Character and 1 Num")
    first_name: str = Field(default=" ",min_length=1, max_length=50)
    last_name: str = Field(default=" ",min_length=1, max_length=50)
    email:str = Field(default=" ",emmin_length=1,max_length=100)

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('Password must contain at least one special character')
        if not re.search(r"\d", value):
            raise ValueError('Password must contain at least one number')
        return value

    @field_validator('email')
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        return value

class UserLoginSchema(BaseModel):
    username: str = Field(default=" ")
    password: str = Field(default=" ")

class UserResponseSchema(BaseResponseModel):
    data:UserRegistrationSchema  
    access_token:str  

     