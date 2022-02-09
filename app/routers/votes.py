from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix= "/votes",
    tags= ["Votes"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(post: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    found_post = db.query(models.Post).filter(models.Post.id == post.post_id).first()
    if not found_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id {post.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == post.post_id, models.Vote.user_id == current_user.id)
    vote = vote_query.first()

    if post.dir:
        if vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"user {current_user.email} alredy voted this post")
        
        else:

            new_vote = models.Vote(user_id = current_user.id, post_id = post.post_id)
            db.add(new_vote)
            db.commit()

            return {"message": "success"}
        
    else:
        if vote:

            vote_query.delete(synchronize_session= False)
            db.commit()

            return {"message": "success"}
            
        else:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user {current_user.email} never voted this post")







