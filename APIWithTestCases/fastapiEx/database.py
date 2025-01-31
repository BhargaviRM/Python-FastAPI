"""
Database connection module for the FastAPI application.

This module sets up the SQLAlchemy engine, session maker, and base class
for declarative models. It also provides a function to get a database
session for use in API endpoints.

Database Configuration:
- Connects to a PostgreSQL database using the specified DATABASE_URL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://postgres:12345@localhost/sampleapi"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Get a database session.

    This function creates a new database session and yields it for use
    in API endpoints. It handles exceptions by rolling back the session
    in case of an error and ensures that the session is closed after use.

    Yields:
        Session: A SQLAlchemy session object for database operations.

    Raises:
        SQLAlchemyError: If an error occurs during database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
