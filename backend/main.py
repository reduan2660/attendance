# Fast API Imports
from typing import Union
from fastapi import Depends, FastAPI, HTTPException

# DB Imports
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine

# DB Migration
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/ping")
def ping():
    return {"Ping": "pong"}

@app.get("/courses")
def get_courses():
    db = SessionLocal()
    courses = db.query(models.Course).all()
    return courses

@app.get("/attendance")
def get_courses():
    db = SessionLocal()
    courses = db.query(models.Attendance).all()
    return courses