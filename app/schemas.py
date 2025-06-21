from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

# --- Cartoon Schemas ---
class CartoonBase(BaseModel):
    title: str
    year: int
    description: Optional[str] = None
    poster_url: HttpUrl
    hero_image_url: Optional[HttpUrl] = None
    video_url: Optional[HttpUrl] = None

class CartoonCreate(CartoonBase):
    pass

class Cartoon(CartoonBase): # Schema for reading/returning a cartoon
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True # For SQLAlchemy model conversion

# --- MovieRequest Schemas ---
class MovieRequestBase(BaseModel):
    movie_name: str
    user_email: EmailStr

class MovieRequestCreate(MovieRequestBase):
    pass

class MovieRequest(MovieRequestBase): # Schema for reading/returning a request
    id: int
    status: str
    requested_at: datetime

    class Config:
        orm_mode = True