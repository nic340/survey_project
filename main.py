from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from models import Survey

sqlite_url = "sqlite:///survey.db"
engine = create_engine(sqlite_url)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"status": "Backend is ready!"}