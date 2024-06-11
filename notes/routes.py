from fastapi import FastAPI,Depends,HTTPException,status
from .schema import NotesCreationSchema,NotesResponseSchema
from .models import get_db_session,Notes
from sqlalchemy.orm import Session

routes = FastAPI()

@routes.post("/notes/",response_model=NotesResponseSchema)
def create_notes(notes_payload:NotesCreationSchema,db:Session=Depends(get_db_session)):
    try:
        new_note = Notes(**notes_payload.model_dump())
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="An unexpected error occurred: " + str(e))
    
    return {"message":"Notes Added Successfully","status":200,"data":new_note}

@routes.post("/notes/{notes_id}",response_model=NotesResponseSchema)
def get_notes_id(notes_id:int,db:Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id==notes_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notes Not Found")
    return {"message":"Note Withdrawn","status":200,"data":note}

@routes.put("/notes/{notes_id}", response_model=NotesResponseSchema)
def update_note(note_id: int, notes_payload: NotesCreationSchema, db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notes Not Found")
    
    for key, value in notes_payload.model_dump().items():
        setattr(note, key, value)

    try:
        db.commit()
        db.refresh(note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    return {"message": "Notes Updated Successfully", "status": 200, "data": note}
    
@routes.delete("/notes/{notes_id}",response_model=NotesResponseSchema)
def delete_note(note_id:int,db:Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id==note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notes Not Found")
    
    try:
        db.delete(note)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    return {"message": "Notes Deleted Successfully", "status": 200, "data": note}
        
    