from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine
from fastapi.middleware.cors import CORSMiddleware
from models import Survey
from typing import List
from sqlmodel import select


sqlite_url = "sqlite:///survey.db"
engine = create_engine(sqlite_url)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"status": "Backend is ready!"}


@app.post("/submit", response_model=Survey)
def submit_survey(survey: Survey):
    with Session(engine) as session:
        session.add(survey)
        session.commit()
        session.refresh(survey)
        return survey

# New Endpoint: View all survey entries
@app.get("/data", response_model=List[Survey])
def read_data():
    with Session(engine) as session:
        surveys = session.exec(select(Survey)).all()
        return surveys