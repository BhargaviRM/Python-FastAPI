
# for installing FastAPI: pip install "fastapi[standard]"
# for installing sqlalchemy: pip install sqlalchemy
# running server: uvicorn main:app --reload
# http://127.0.0.1:8000 
# for flagger (http://127.0.0.1:8000/docs)

from fastapi import FastAPI
from .router import router
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
