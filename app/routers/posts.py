from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

@router.get("/", response_model= List[schemas.PostOut])
def send_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): 

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id= current_user.id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 

    return new_post




@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {id} was not found")
    
    return post



@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    delete_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if delete_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {id} was not found")

    if not delete_post.owner_id == current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"post with id {id} was not yours to delete")
    
    delete_post.delete(synchronize_session= False)
    # delete_post.delete(synchronize_session= False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    update_post = db.query(models.Post).filter(models.Post.id == id).first()

    if update_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {id} was not found")
    
    if not update_post.owner_id == current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"post with id {id} was not yours to update")
    
    update_post.update(post.dict(), synchronize_session= False)
    db.commit()
    
    return update_post.first()