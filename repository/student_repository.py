# ==========================================
# Repository  ->  database work only (queries)
# ==========================================
from sqlalchemy.orm import Session
from model.student import Students


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_student(self):
        return self.db.query(Students).all()

    def get_student_by_roll(self, roll: int):
        return self.db.query(Students).filter(Students.roll == roll).first()

    def create_student(self, student: Students):
        self.db.add(student)

    def delete_student(self, student: Students):
        self.db.delete(student)
