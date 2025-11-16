from datetime import time
from typing import Optional, Literal

from pydantic import BaseModel,EmailStr


class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(Post):
    pass

class VotePostResponse(Post):
    id : int
    created_at : time
    user_id : int
    vote : int

class PostResponse(Post):
    id : int
    created_at : time
    user_id : int


class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int]

class Vote(BaseModel):
    post_id : int
    dir : Literal[0,1]




