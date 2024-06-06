from pydantic import BaseModel, Field, ValidationError, field_validator
import re

class UserRegistrationSchema(BaseModel):
    username: str = Field(pattern=r"^[a-zA-Z0-9.]{3,15}$")
    password: str = Field(min_length=8, max_length=50,description="Minimun 8 long,1 Caps, 1 Special Character and 1 Num")
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('Password must contain at least one special character')
        if not re.search(r"\d", value):
            raise ValueError('Password must contain at least one number')
        return value

class UserResponseSchema(BaseModel):
    id: int
    username: str
    password: str
    first_name: str
    last_name: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('Password must contain at least one special character')
        if not re.search(r"\d", value):
            raise ValueError('Password must contain at least one number')
        return value

class UserLoginSchema(BaseModel):
    username: str
    password: str

     