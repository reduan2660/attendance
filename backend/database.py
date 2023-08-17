from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Environment Variables
import os
from dotenv import load_dotenv
load_dotenv() 

#  DB Credentials
DB_HOST     =os.getenv("DB_HOST")
DB_NAME     =os.getenv("DB_NAME")
DB_USER     =os.getenv("DB_USER")
DB_PASSWORD =os.getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
