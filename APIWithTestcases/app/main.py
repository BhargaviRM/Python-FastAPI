"""
Main entry point for the FastAPI application.

This module initializes the FastAPI application, sets up the database
connection, and includes the API router for handling task-related
endpoints. It creates the database tables defined in the SQLAlchemy
models if they do not already exist.

Usage:
    Run the application using a command like:
    uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapiEx.router import router
from fastapiEx.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
