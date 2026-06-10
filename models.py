# database/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, TIMESTAMP
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class ResumeHistory(Base):
    __tablename__ = "resume_history"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, nullable=False)
    job_title = Column(String(100), nullable=False)
    extracted_skills = Column(Text)
    match_score = Column(Integer)
    missing_skills = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
