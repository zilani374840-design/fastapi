# Subjects table -> marks of each student (by roll) in each subject
from sqlalchemy import Column, Integer
from db import base


class Subjects(base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_roll = Column(Integer, unique=True)
    english_score = Column(Integer)
    math_score = Column(Integer)
    history_score = Column(Integer)
