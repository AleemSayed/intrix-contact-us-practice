
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Check whether database URL exists
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
