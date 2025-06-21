from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession # Keep for type hinting if needed elsewhere

from database import create_db_and_tables, AsyncSessionLocal # Import AsyncSessionLocal
from routers import cartoons, movie_requests
import crud, schemas # For initial data
from contextlib import asynccontextmanager
import logging
from prometheus_fastapi_instrumentator import Instrumentator


# Sample cartoon data
# Ensure poster_url, hero_image_url, and video_url are valid strings that Pydantic's HttpUrl can parse.
sample_cartoons_data = [

    {
        "title": "Test Clip WA0064 (Temporary Link)", # Your test clip
        "year": 2024,
        "description": "A test video clip using a temporary signed URL. This link will expire if it's a signed URL. Use a permanent public URL for long-term.",
        "poster_url": "https://via.placeholder.com/220x330.png?text=Test+Clip",
        "hero_image_url": None,
        "video_url": "https://lqladjqxlnoycsjygnro.supabase.co/storage/v1/object/sign/retro-movies/VID-20250609-WA0064_web.mp4?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9hZjkzOTZhZi1iNDk2LTQ4NTItOWFkMy0zODdhMDZlYzYyOTMiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJyZXRyby1tb3ZpZXMvVklELTIwMjUwNjA5LVdBMDA2NF93ZWIubXA0IiwiaWF0IjoxNzQ5ODU0NjUyLCJleHAiOjE3NTA0NTk0NTJ9.UCV0IVRXU3dusxl05Ixiw9JzgA9yFKDKAKZyts-bST0" # Replace with permanent public URL if possible
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Handles application startup and shutdown events. """
    logging.info("--- Lifespan: Startup sequence initiated ---")
    
    # ### BEST PRACTICE: Moved logic from on_startup() here
    print("--- Lifespan: Calling create_db_and_tables ---")
    await create_db_and_tables()
    
    print("--- Lifespan: Calling populate_initial_data ---")
    await populate_initial_data()
    
    logging.info("--- Lifespan: Startup complete. Application is ready. ---")
    yield
    logging.info("--- Lifespan: Shutdown complete. ---")



app = FastAPI(title="RetroToons API",lifespan=lifespan) # Ensure app is defined before middleware
Instrumentator().instrument(app).expose(app)
# CORS Middleware
origins = [
    "http://localhost:5173",    # <--- ADD THIS LINE! Your frontend origin
    "http://127.0.0.1:5173",    # Good to add this too, as localhost can resolve to 127.0.0.1
    "http://localhost:3000",    # Keep if you might use this port for other frontend dev
    "http://127.0.0.1:3000",    # Keep if you might use this port
    # Add your frontend's production URL here when you eventually deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # This is fine since you are listing specific origins
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)


async def populate_initial_data():
    """Populates the database with sample cartoons if they don't exist."""
    print("Attempting to populate initial data...")
    # Get a new session specifically for this task, independent of request sessions
    async with AsyncSessionLocal() as db:
        for cartoon_data in sample_cartoons_data:
            existing_cartoon = await crud.get_cartoon_by_title(db, title=cartoon_data["title"])
            if not existing_cartoon:
                try:
                    # Validate with Pydantic schema before creating
                    cartoon_schema = schemas.CartoonCreate(**cartoon_data)
                    # crud.create_cartoon now handles its own commit
                    await crud.create_cartoon(db=db, cartoon=cartoon_schema)
                    print(f"Added: {cartoon_data['title']}")
                except Exception as e:
                    print(f"Error adding {cartoon_data['title']}: {e}")
                    # If an error occurs, it's logged, and the loop continues to the next cartoon.
                    # The transaction for the failed cartoon should be rolled back within crud.create_cartoon
                    # if the commit there fails, or by SQLAlchemy's default behavior within the session block.
                    # To be extremely safe, you could add an explicit db.rollback() here in the except,
                    # but since crud.create_cartoon now commits, the scope of failure is smaller.
                    # If crud.create_cartoon itself raises an unhandled exception before its commit,
                    # the outer session 'db' here might still be fine for the next iteration.
            else:
                print(f"Skipped (already exists): {cartoon_data['title']}")
    print("Initial data population check complete.")


@app.on_event("startup")
async def on_startup():
    print("Application startup...")
    # --- BEGIN DEBUG from database.py (moved here for clarity as it's a startup task) ---
    print("--- main.py/on_startup: Calling create_db_and_tables ---")
    # --- END DEBUG ---
    await create_db_and_tables()
    # --- BEGIN DEBUG ---
    print("--- main.py/on_startup: Calling populate_initial_data ---")
    # --- END DEBUG ---
    await populate_initial_data()
    print("Startup complete.")

app.include_router(cartoons.router)
app.include_router(movie_requests.router)

@app.get("/api/health")
async def root():
    return {"message": "RetroToons API is healthy!"}