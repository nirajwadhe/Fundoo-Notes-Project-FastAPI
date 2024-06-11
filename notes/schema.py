from pydantic import BaseModel,Field
from typing import Optional,List
from datetime import datetime

class BaseResponseModel(BaseModel):
    message:str
    status:int

class NotesCreationSchema(BaseModel):
    description:str = Field(default="",max_length=1000) 
    title: str = Field(default="", max_length=255)
    color: Optional[str] = Field(None, max_length=50)
    remainder: Optional[datetime] = None
    is_archive: bool
    is_trash_bool: bool
    


class NotesResponseSchema(BaseResponseModel):
    data: NotesCreationSchema
    
class NotesReadSchema(BaseModel):
    notes_id: int
    title: str
    description: str
    color: str
    remainder: Optional[datetime] = None
    is_archive: bool
    is_trash_bool: bool
    user_id: int
        
# class NotesListResponseSchema(BaseResponseModel):
#     data: List[NotesReadSchema]

class NotesUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    color: Optional[str] = Field(None, max_length=50)
    remainder: Optional[datetime] = None
    is_archive: Optional[bool] = None
    is_trash_bool: Optional[bool] = None    