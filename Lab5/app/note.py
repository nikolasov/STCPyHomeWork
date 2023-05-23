from . import  models,schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import insert, select, update
import json

router = APIRouter()
@router.get('/api/tests')
def get_notes(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''): 
    skip = (page - 1) * limit
    notes = db.query(models.Task.id, models.Task.name, models.Task.status, models.Category.name, models.Task.description).join(models.Category).limit(limit).offset(skip).all()

    return {'status': 'success', 'results': len(notes), 'notes': notes}
     

@router.post('/api/tests', status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.TaskBaseSchema, db: Session = Depends(get_db)):
    print(payload.dict())
    new_note = models.Task(**payload.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"status": "success", "note": new_note}


@router.patch('/api/tests/{taskId}')
def update_note(taskId: str, payload: schemas.TaskBaseSchema, db: Session = Depends(get_db)):
    print(payload.dict())
    note_query = db.query(models.Task).filter(models.Task.id == taskId)
    db_note = note_query.first()

    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {taskId} found')
    update_data = payload.dict(exclude_unset=True)
    note_query.filter(models.Task.id == taskId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_note)
    return {"status": "success", "note": db_note}


@router.get('/api/tests/{taskId}')
def get_post(taskId: str, db: Session = Depends(get_db)):
    note = db.query(models.Task).filter(models.Task.id == taskId).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {id} found")
    return {"status": "success", "note": note}


@router.delete('/api/tests/{taskId}')
def delete_post(taskId: str, db: Session = Depends(get_db)):
    note_query = db.query(models.Task).filter(models.Task.id == taskId)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)