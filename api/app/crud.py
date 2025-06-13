# In retrotoons_api/app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func # for random order_by
from . import models, schemas
from typing import List, Optional

# --- Cartoon CRUD ---

# ... (get_cartoon, get_cartoons, create_cartoon should already be here) ...
# Ensure create_cartoon looks like this from our previous fix:
async def create_cartoon(db: AsyncSession, cartoon: schemas.CartoonCreate) -> models.Cartoon:
    cartoon_data_for_db = cartoon.dict()
    if cartoon_data_for_db.get("poster_url"):
        cartoon_data_for_db["poster_url"] = str(cartoon.poster_url)
    if cartoon_data_for_db.get("hero_image_url"):
        cartoon_data_for_db["hero_image_url"] = str(cartoon.hero_image_url) if cartoon.hero_image_url else None
    if cartoon_data_for_db.get("video_url"):
        cartoon_data_for_db["video_url"] = str(cartoon.video_url) if cartoon.video_url else None
    
    db_cartoon = models.Cartoon(**cartoon_data_for_db)
    db.add(db_cartoon)
    await db.commit() # Commit this specific cartoon
    await db.refresh(db_cartoon)
    return db_cartoon

# --- ADD OR VERIFY THESE FUNCTIONS ---
async def get_featured_cartoon(db: AsyncSession) -> Optional[models.Cartoon]:
    # Prioritize cartoons with a hero_image_url, then pick one randomly if multiple,
    # or pick any cartoon randomly if none have hero_image_url
    query_with_hero = select(models.Cartoon).filter(models.Cartoon.hero_image_url.isnot(None)).order_by(func.random()).limit(1)
    result = await db.execute(query_with_hero)
    featured = result.scalars().first()
    if not featured:
        # If no cartoon has a hero_image_url, pick any cartoon randomly
        query_any = select(models.Cartoon).order_by(func.random()).limit(1)
        result_any = await db.execute(query_any)
        featured = result_any.scalars().first()
    return featured

async def get_classic_cartoons(db: AsyncSession, limit: int = 8) -> List[models.Cartoon]:
    # Example: Classics are before 1960
    result = await db.execute(
        select(models.Cartoon)
        .filter(models.Cartoon.year < 1960)
        .order_by(models.Cartoon.year.desc(), models.Cartoon.title) # Or func.random() for variety
        .limit(limit)
    )
    return result.scalars().all()

async def get_golden_age_cartoons(db: AsyncSession, limit: int = 8) -> List[models.Cartoon]:
    # Example: Golden Age 1930-1959
    result = await db.execute(
        select(models.Cartoon)
        .filter(models.Cartoon.year >= 1930, models.Cartoon.year <= 1959)
        .order_by(models.Cartoon.year.desc(), models.Cartoon.title) # Or func.random()
        .limit(limit)
    )
    return result.scalars().all()

async def search_cartoons(db: AsyncSession, query: str, limit: int = 20) -> List[models.Cartoon]:
    # Ensure this function is also present if your search endpoint uses it
    result = await db.execute(
        select(models.Cartoon)
        .filter(models.Cartoon.title.ilike(f"%{query}%")) # Case-insensitive search
        .order_by(models.Cartoon.year.desc(), models.Cartoon.title)
        .limit(limit)
    )
    return result.scalars().all()
# --- END ADD OR VERIFY ---


# --- MovieRequest CRUD ---
async def create_movie_request(db: AsyncSession, request: schemas.MovieRequestCreate) -> models.MovieRequest:
    db_request = models.MovieRequest(**request.dict())
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request

async def get_movie_requests(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.MovieRequest]:
    result = await db.execute(select(models.MovieRequest).offset(skip).limit(limit))
    return result.scalars().all()

# Helper for initial data
async def get_cartoon_by_title(db: AsyncSession, title: str) -> Optional[models.Cartoon]:
    result = await db.execute(select(models.Cartoon).filter(models.Cartoon.title == title))
    return result.scalars().first()