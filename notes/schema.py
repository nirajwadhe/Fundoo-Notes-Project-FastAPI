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
        
    class Config:
        from_attributes = True

class NotesUpdateResponseSchema(NotesCreationSchema):
    is_archive: bool
    is_trash_bool: bool
    user_id: int
    notes_id: int
    
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
    labels : list[str] = []
    
    class Config():
        from_attributes=True
        
class NotesReadSchemaWithLabel(BaseModel):
    notes_id: int
    title: str
    description: str
    color: str
    remainder: Optional[datetime] = None
    is_archive: bool
    is_trash_bool: bool
    user_id: int
        
    class Config():
        from_attributes=True
 
class NotesListResponseSchema(BaseResponseModel):
    data: List[NotesReadSchema]

class NotesTrashResponseSchema(BaseResponseModel):
    data : List[NotesReadSchemaWithLabel]
    
class NotesUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    color: Optional[str] = Field(None, max_length=50)
    remainder: Optional[datetime] = None  
 
class LabelCreationSchema(BaseModel):
    label_name: str

class LabelsReadSchema(BaseModel):
    labels_id: int
    label_name: str
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
    
class LabelResponseSchema(BaseResponseModel):
    data: LabelsReadSchema

class LabelsListResponseSchema(BaseResponseModel):
    data: List[LabelsReadSchema]