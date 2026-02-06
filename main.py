from typing import List
from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel, create_engine
from fastapi.middleware.cors import CORSMiddleware
from models import Survey

sqlite_url = "sqlite:///survey.db"
engine = create_engine(sqlite_url)

app = FastAPI()

# --- NEW: Allow the HTML frontend to talk to this backend ---
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

# --- NEW: Submit a survey (POST) ---
@app.post("/surveys/", response_model=Survey)
def create_survey(survey: Survey):
    with Session(engine) as session:
        session.add(survey)
        session.commit()
        session.refresh(survey)
        return survey

# --- NEW: View all surveys (GET) ---
@app.get("/surveys/", response_model=List[Survey])
def read_surveys():
    with Session(engine) as session:
        surveys = session.exec(select(Survey)).all()
        return surveys