from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import HTTPException, status
import sqlalchemy as db
import os
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
sqlite_database = os.getenv('DB_SOUND_STUDIO')

# Construct the database connection string
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{sqlite_database}.db"

# Create a database engine
engine = db.create_engine(SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Define a base for declarative models
Base = declarative_base()

# Define a FastAPI dependency to get a database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    finally:
        db.close()
