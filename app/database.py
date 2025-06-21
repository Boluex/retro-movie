# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# from .models import Base # Import Base from models

# load_dotenv() # Load variables from .env file

# DATABASE_URL = 'postgresql://postgres:admin123@localhost:5432/retrovideos'

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable not set.")

# engine = create_async_engine(DATABASE_URL, echo=True) # echo=True for dev logging

# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
#     autocommit=False,
#     autoflush=False,
# )

# async def get_db() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             await session.close()

# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all) # Use with caution: drops all tables
#         await conn.run_sync(Base.metadata.create_all)
#     print("Database tables created (if they didn't exist).")











import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base # Import Base from models

# --- BEGIN DEBUG ---
print("--- database.py: Attempting to load .env ---")
# --- END DEBUG ---

load_dotenv() # Load variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")

# --- BEGIN DEBUG ---
print(f"--- database.py: DATABASE_URL from environment: {DATABASE_URL} ---")
# --- END DEBUG ---


if not DATABASE_URL:
    # --- BEGIN DEBUG ---
    print("--- database.py: ERROR: DATABASE_URL environment variable not set. ---")
    # --- END DEBUG ---
    raise ValueError("DATABASE_URL environment variable not set.")

# --- BEGIN DEBUG ---
print(f"--- database.py: Attempting to create engine with URL: {DATABASE_URL} ---")
# --- END DEBUG ---

engine = create_async_engine(DATABASE_URL, echo=True) # echo=True for dev logging

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # --- BEGIN DEBUG ---
    print("--- database.py: Database tables created (if they didn't exist). ---")
    # --- END DEBUG ---