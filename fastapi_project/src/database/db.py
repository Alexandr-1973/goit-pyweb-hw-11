# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/rest_app"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.conf.config import DB_URL

# DATABASE_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/rest_app"

engine = create_async_engine(DB_URL)

SessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)

async def get_db():
    async with SessionLocal() as session:
        yield session