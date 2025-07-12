from fastapi import FastAPI
from database import create_db_and_tables, engine
from sqlmodel import Session, select
from models import Contact, ContactCreate

app = FastAPI()

create_db_and_tables()

@app.get("/")
def root():
    return {"Hello": "World!"}