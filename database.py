from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config.configs import config

from sqlalchemy.ext.declarative import declarative_base

POSTGRES_USER     = config.POSTGRES_USER
POSTGRES_PORT     = config.POSTGRES_PORT
POSTGRES_HOST     = config.POSTGRES_HOST
POSTGRES_PASSWORD = config.POSTGRES_PASSWORD
POSTGRES_DATABASE = config.POSTGRES_DATABASE

DATABASE_URL       = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
