from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db



router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)




@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User wiht email id {user.email} already exists")

    # Hash the user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user



@router.get("/", response_model= List[schemas.UserResponse])
def send_users(db: Session = Depends(get_db)): 

    users = db.query(models.User).all()

    return users



@router.get("/{id}", response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id {id} was not found")
    
    return user