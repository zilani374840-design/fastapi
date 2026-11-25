# Students table
from sqlalchemy import Column, Integer, String
from db import base


class Students(base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    email = Column(String(100))
    roll = Column(Integer, unique=True)
    session = Column(String(20))
