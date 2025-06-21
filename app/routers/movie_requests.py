from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import crud, models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/movie-requests",
    tags=["movie_requests"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.MovieRequest, status_code=201)
async def create_new_movie_request(
    request: schemas.MovieRequestCreate, db: AsyncSession = Depends(get_db)
):
    # Could add validation here, e.g., if a movie with this name already exists or is requested
    return await crud.create_movie_request(db=db, request=request)

@router.get("/", response_model=List[schemas.MovieRequest])
async def read_all_movie_requests(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    # This should be an admin-only endpoint in a real application
    requests = await crud.get_movie_requests(db, skip=skip, limit=limit)
    return requests