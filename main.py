from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import engine, SessionLocal, Base

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/notes", response_model=List[schemas.ShowNote],status_code=status.HTTP_200_OK)
def read_all_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes

@app.get("/notes/{note_id}", status_code=status.HTTP_200_OK)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )
    return note

@app.post("/notes", status_code=status.HTTP_201_CREATED)
def create_note(request: schemas.Note, db: Session = Depends(get_db)):
    new_note = models.Note(title=request.title, content=request.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(note_id: int, request: schemas.Note, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )
    note.title = request.title
    note.content = request.content
    db.commit()
    return note

@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )
    db.delete(note)
    db.commit()
    return {"message": f"Note {note_id} deleted successfully"}
