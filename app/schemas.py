from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime



class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True




class UserLogin(BaseModel):
    email: EmailStr
    password: str




class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True







class AccessToken(BaseModel):
    access_token: str
    token_type: str

class Token(BaseModel):
    id: Optional[str] = None






class Vote(BaseModel):
    post_id: int
    dir: bool