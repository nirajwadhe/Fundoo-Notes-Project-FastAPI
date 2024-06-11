from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class BaseResponseModel(BaseModel):
    message:str
    status:int

class NotesCreationSchema(BaseModel):
    description:str = Field(default="",max_length=1000) 
    title: str = Field(default="", max_length=255)
    color: Optional[str] = Field(None, max_length=50)
    remainder: Optional[datetime] = None
    user_id:int = Field(default_factory=int)

class NotesResponseSchema(BaseResponseModel):
    data: NotesCreationSchema