from fastapi import FastAPI,Depends,HTTPException,status,Security,Request
from fastapi.security import APIKeyHeader
from .schema import NotesCreationSchema,NotesResponseSchema,BaseResponseModel,NotesUpdateSchema,NotesListResponseSchema,LabelCreationSchema,LabelsListResponseSchema,LabelResponseSchema
from .models import get_db_session,Notes,Labels
from sqlalchemy.orm import Session
from .notes_utils import auth_user
from core.logger_config import logger_config,USER_LOG
from core import create_app

routes = create_app(name="notes",dependencies=[Security(APIKeyHeader(name="Authorization")),Depends(auth_user)])
logger = logger_config(USER_LOG)

@routes.post("/notes/",response_model=NotesResponseSchema)
def create_notes(request:Request,notes_payload:NotesCreationSchema,db:Session=Depends(get_db_session)):
    try:
        new_note = Notes(**notes_payload.model_dump(),user_id=request.state.user_id)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        logger.info("Notes Created Succesfully!!")
    except HTTPException as e:
        db.rollback()
        logger.error(f"HTTPException: {e}")
        raise HTTPException(status_code=500,detail="An unexpected error occurred: " + str(e))
    return {"message":"Notes Added Successfully","status":200,"data":new_note}

@routes.get("/notes/read_notes", response_model=NotesListResponseSchema)
def read_notes_id(request: Request, db: Session = Depends(get_db_session)):
    notes = db.query(Notes).filter(Notes.user_id == request.state.user_id).all()
    if not notes:
        logger.warning("Notes Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notes Not Found")
    logger.info("Notes Retrieved Successfully")
    return {"message":"Get_Trash","status":200,"data":notes}

@routes.put("/notes/{notes_id}", response_model=NotesResponseSchema)
def update_note(request:Request, notes_id:int,notes_payload: NotesUpdateSchema, db: Session = Depends(get_db_session)):
    notes = db.query(Notes).filter(Notes.notes_id == notes_id,Notes.user_id==request.state.user_id).first()
    if not notes:
        logger.warning(f"Notes with ID {notes_id} Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notes Not Found")
    update_data=notes_payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(notes, key, value)
    try:
        db.commit()
        db.refresh(notes)
        logger.info(f"Notes with ID {notes_id} Updated Successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while updating note: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    return {"message": "Notes Updated Successfully", "status": 200, "data": notes}
    
@routes.delete("/notes/{notes_id}",response_model=BaseResponseModel)
def delete_note(request:Request , notes_id:int,db:Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id==notes_id,Notes.user_id==request.state.user_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Notes Not Found")
    try:
        db.delete(note)
        db.commit()
        logger.info(f"Notes with ID {notes_id} Deleted Successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while deleting note: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    return {"message": "Notes Deleted Successfully", "status": 200, "data": note}

@routes.patch("/notes/{notes_id}/archive", response_model=NotesResponseSchema)
def set_archive(request: Request, notes_id: int, archive: bool, db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id == notes_id, Notes.user_id == request.state.user_id).first()
    if not note:
        logger.warning(f"Note with ID {notes_id} Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    try:
        if archive:
            note.is_archive = True  
        else:
            note.is_archive = False 
        db.commit()
        db.refresh(note)
        logger.info(f"Note with ID {notes_id} Archive Status Changed to {archive}")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while setting archive status: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: " + str(e))
    return {"message":"Archived status Chan ged", "status": 200, "data": note}

@routes.patch("/notes/{notes_id}/trash", response_model=NotesResponseSchema)
def set_trash(request: Request, notes_id: int, trash: bool, db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.notes_id == notes_id, Notes.user_id == request.state.user_id).first()
    if not note:
        logger.warning(f"Note with ID {notes_id} Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    try:
        if trash:
            note.is_trash_bool = True  
        else:
            note.is_trash_bool = False 
        db.commit()
        db.refresh(note)
        logger.info(f"Note with ID {notes_id} Trash Status Changed to {trash}")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while setting trash status: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: " + str(e))
    return {"message":"Archived status Chan ged", "status": 200, "data": note}

@routes.get("/notes/archive", response_model=NotesListResponseSchema)
def get_archive(request: Request,db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.user_id == request.state.user_id,Notes.is_archive == True,Notes.is_trash_bool==False).all()
    if not note:
        logger.warning("No Archived Notes Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    logger.info("Archived Notes Retrieved Successfully")
    return {"message":"Get_Trash","status":200,"data":note}

@routes.get("/notes/trash", response_model=NotesListResponseSchema)
def get_trash(request: Request,db: Session = Depends(get_db_session)):
    note = db.query(Notes).filter(Notes.user_id == request.state.user_id,Notes.is_trash_bool == True).all()
    if not note:
        logger.warning("No Trashed Notes Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note Not Found")
    logger.info("Trashed Notes Retrieved Successfully")
    return {"message":"Get_Trash","status":200,"data":note}
        
@routes.post("/labels/",response_model=LabelResponseSchema)
def create_labels(request:Request,labels_payload:LabelCreationSchema,db:Session=Depends(get_db_session)):
    try:
        new_note = Labels(**labels_payload.model_dump(),user_id=request.state.user_id)
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        logger.info("Labels Added Successfully")
    except HTTPException as e:
        db.rollback()
        logger.error(f"HTTPException: {e}")
        raise HTTPException(status_code=500,detail="An unexpected error occurred: " + str(e))
    return {"message":"Labels Added Successfully","status":200,"data":new_note} 
    
@routes.get("/labels/read_labels", response_model=LabelsListResponseSchema)
def read_labels(request: Request, db: Session = Depends(get_db_session)):
    labels = db.query(Labels).filter(Labels.user_id == request.state.user_id).all()
    if not labels:
        logger.warning("Labels Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notes Not Found")
    logger.info("Labels Retrieved Successfully")
    return {"message":"Get_Trash","status":200,"data":labels}    

@routes.put("/labels/{labels_id}", response_model=LabelResponseSchema)
def update_label(request:Request, labels_id:int,label_payload:LabelCreationSchema, db: Session = Depends(get_db_session)):
    labels = db.query(Labels).filter(Labels.labels_id == labels_id,Labels.user_id==request.state.user_id).first()
    if not labels:
        logger.warning(f"Label with ID {labels_id} Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Labels Not Found")
    update_data=label_payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(labels, key, value)
    try:
        db.commit()
        db.refresh(labels)
        logger.info(f"Labels with ID {labels_id} Updated Successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while updating label: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    return {"message": "Notes Updated Successfully", "status": 200, "data":labels}

@routes.delete("/labels/{labels_id}",response_model=BaseResponseModel)
def delete_labels(request:Request , labels_id:int,db:Session = Depends(get_db_session)):
    label = db.query(Labels).filter(Labels.labels_id==labels_id,Labels.user_id==request.state.user_id).first()
    if not label:
        logger.warning(f"Label with ID {labels_id} Not Found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Labels Not Found")
    try:
        db.delete(label)
        db.commit()
        logger.info(f"Label with ID {labels_id} Deleted Successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while deleting label: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    return {"message": "Labels Deleted Successfully", "status": 200, "data": label}