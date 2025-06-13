from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/cartoons",
    tags=["cartoons"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Cartoon, status_code=201)
async def create_new_cartoon(
    cartoon: schemas.CartoonCreate, db: AsyncSession = Depends(get_db)
):
    # In a real app, this would be admin-protected
    db_cartoon = await crud.get_cartoon_by_title(db, title=cartoon.title)
    if db_cartoon:
        raise HTTPException(status_code=400, detail="Cartoon with this title already exists")
    return await crud.create_cartoon(db=db, cartoon=cartoon)

@router.get("/", response_model=List[schemas.Cartoon])
async def read_cartoons(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    cartoons = await crud.get_cartoons(db, skip=skip, limit=limit)
    return cartoons

@router.get("/search", response_model=List[schemas.Cartoon])
async def search_for_cartoons(
    query: str = Query(..., min_length=1, description="Search query for cartoon titles"),
    db: AsyncSession = Depends(get_db)
):
    cartoons = await crud.search_cartoons(db, query=query)
    if not cartoons:
        raise HTTPException(status_code=404, detail="No cartoons found matching your query")
    return cartoons

@router.get("/featured", response_model=Optional[schemas.Cartoon])
async def read_featured_cartoon(db: AsyncSession = Depends(get_db)):
    cartoon = await crud.get_featured_cartoon(db)
    if cartoon is None:
        # Fallback if no cartoons exist at all, or handle as needed
        raise HTTPException(status_code=404, detail="No featured cartoon available")
    return cartoon

@router.get("/sections/classics", response_model=List[schemas.Cartoon])
async def read_classic_cartoons(limit: int = 8, db: AsyncSession = Depends(get_db)):
    cartoons = await crud.get_classic_cartoons(db, limit=limit)
    return cartoons

@router.get("/sections/golden-age", response_model=List[schemas.Cartoon])
async def read_golden_age_cartoons(limit: int = 8, db: AsyncSession = Depends(get_db)):
    cartoons = await crud.get_golden_age_cartoons(db, limit=limit)
    return cartoons

@router.get("/{cartoon_id}", response_model=schemas.Cartoon)
async def read_cartoon_by_id(cartoon_id: int, db: AsyncSession = Depends(get_db)):
    db_cartoon = await crud.get_cartoon(db, cartoon_id=cartoon_id)
    if db_cartoon is None:
        raise HTTPException(status_code=404, detail="Cartoon not found")
    return db_cartoon