from fastapi import FastAPI,Depends,HTTPException,status,Security,Request
from fastapi.security import APIKeyHeader
from .schema import NotesCreationSchema,NotesResponseSchema,BaseResponseModel,NotesReadSchema,NotesUpdateSchema,NotesListResponseSchema
from .models import get_db_session,Notes
from sqlalchemy.orm import Session
from .notes_utils import auth_user
from typing import List

routes = FastAPI(dependencies=[Security(APIKeyHeader(name="Authorization")),Depends(auth_user)])

@routes.post("/notes/",response_model=NotesResponseSchema)
def create_notes(request:Request,notes_payload:NotesCreationSchema,db:Session=Depends(get_db_session)):
    try:
        new_note = Notes(**notes_payload.model_dump(),user_id=request.state.user_id)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="An unexpected error occurred: " + str(e))
    return {"message":"Notes Added Successfully","status":200,"data":new_note}

@routes.get("/notes/read_notes", response_model=List[NotesReadSchema])
def read_notes_id(request: Request, db: Session = Depends(get_db_session)):
    notes = db.query(Notes).filter(Notes.user_id == request.state.user_id).all()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notes Not Found")
    # print(type(notes))
    # return {"message":"Note Fetched","status":200,"data":[NotesReadSchema.model_validate(note).model_dump() for note in notes]}
    return notes

@routes.put("/notes/{notes_id}", response_model=NotesResponseSchema)
def update_note(request:Request, notes_id:int,notes_payload: NotesUpdateSchema, db: Session = Depends(get_db_session)):
    notes = db.query(Notes).filter(Notes.notes_id == notes_id,Notes.user_id==request.state.user_id).first()
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notes Not Found")
    update_data=notes_payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(notes, key, value)
    try:
        db.commit()
        db.refresh(notes)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    return {"message": "Notes Updated Successfully", "status": 200, "data": notes}
    
@routes.delete("/notes/{notes_id}",response_model=BaseResponseModel)
def delete_note(request:Request , note_id:int,db:Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id==note_id,Notes.user_id==request.state.user_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notes Not Found")
    try:
        db.delete(note)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    return {"message": "Notes Deleted Successfully", "status": 200, "data": note}

@routes.patch("/notes/{notes_id}/archive", response_model=NotesResponseSchema)
def set_archive(request: Request, notes_id: int, archive: bool, db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id == notes_id, Notes.user_id == request.state.user_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    try:
        if archive:
            note.is_archive = True  
        else:
            note.is_archive = False 
        db.commit()
        db.refresh(note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: " + str(e))
    return {"message":"Archived status Chan ged", "status": 200, "data": note}

@routes.patch("/notes/{notes_id}/trash", response_model=NotesResponseSchema)
def set_trash(request: Request, notes_id: int, trash: bool, db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id == notes_id, Notes.user_id == request.state.user_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    try:
        if trash:
            note.is_trash_bool = True  
        else:
            note.is_trash_bool = False 
        db.commit()
        db.refresh(note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: " + str(e))
    return {"message":"Archived status Chan ged", "status": 200, "data": note}

@routes.get("/notes/archive", response_model=List[NotesListResponseSchema])
def get_archive(request: Request,db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.user_id == request.state.user_id,Notes.is_archive == True,Notes.is_trash_bool==False).all()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    return note

@routes.get("/notes/trash", response_model=List[NotesReadSchema])
def get_trash(request: Request,db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.user_id == request.state.user_id,Notes.is_trash_bool == True).all()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    return note
        
    