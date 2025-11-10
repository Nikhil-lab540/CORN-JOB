from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "Users_student"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    phone_number = Column(String)

class Homework(Base):
    __tablename__ = "myapp_homework"
    id = Column(Integer, primary_key=True)
    homework_code = Column(String)

class HomeworkSubmission(Base):
    __tablename__ = "myapp_homeworksubmission"
    id = Column(Integer, primary_key=True)
    student_id = Column(String)  # varchar type in DB
    homework_id = Column(Integer, ForeignKey("myapp_homework.id"))
    submission_date = Column(DateTime)
    agent_analysis_data = Column(Text)
