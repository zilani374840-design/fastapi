# ==========================================
# Repository  ->  queries for the subjects table
# ==========================================
from sqlalchemy.orm import Session
from model.subjects import Subjects


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_course_by_roll(self, roll: int):
        return self.db.query(Subjects).filter(Subjects.student_roll == roll).first()

    def add_subject_score(self, subject: Subjects):
        self.db.add(subject)

    def delete_subject_score(self, subject: Subjects):
        self.db.delete(subject)
