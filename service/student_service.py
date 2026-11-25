# ==========================================
# Service  ->  Business logic (calculations, checks, rules)
# ==========================================
from fastapi import HTTPException
from sqlalchemy.orm import Session

from model.student import Students
from model.subjects import Subjects
from repository.student_repository import StudentRepository
from repository.course_repository import CourseRepository
from utils.schema import StudentCreate, StudentUpdate, StudentResponse


# Returns a comment based on the average marks
def get_comment(average: float) -> str:
    if average >= 90:
        return "Excellent"
    elif average >= 80:
        return "Very Good"
    elif average >= 70:
        return "Good"
    else:
        return "Need Improvement"


class StudentService:
    def __init__(self, db: Session):
        self.db = db
        self.student_repository = StudentRepository(db)
        self.course_repository = CourseRepository(db)

    # Combines a student and their marks into one response
    def make_response(self, student: Students) -> StudentResponse:
        score = self.course_repository.get_course_by_roll(student.roll)

        # If there are no marks, use 0 (so nothing crashes)
        english = score.english_score if score else 0
        math = score.math_score if score else 0
        history = score.history_score if score else 0

        average = round((english + math + history) / 3, 2)

        return StudentResponse(
            id=student.id,
            name=student.name,
            age=student.age,
            email=student.email,
            roll=student.roll,
            session=student.session,
            english_score=english,
            math_score=math,
            history_score=history,
            average=average,
            comment=get_comment(average),
        )

    # Finds a student by roll, raises a 404 error if not found
    def find_student_or_404(self, roll: int) -> Students:
        student = self.student_repository.get_student_by_roll(roll)
        if student is None:
            raise HTTPException(status_code=404, detail=f"No student found with roll {roll}")
        return student

    # ---------- READ ----------
    def get_students(self):
        students = self.student_repository.get_all_student()
        return [self.make_response(student) for student in students]

    def get_student(self, roll: int):
        student = self.find_student_or_404(roll)
        return self.make_response(student)

    # ---------- CREATE ----------
    def add_student(self, payload: StudentCreate):
        # Check whether this roll already exists
        if self.student_repository.get_student_by_roll(payload.roll):
            raise HTTPException(status_code=400, detail=f"Roll {payload.roll} already exists")

        student = Students(
            name=payload.name,
            age=payload.age,
            email=payload.email,
            roll=payload.roll,
            session=payload.session,
        )
        subject = Subjects(
            student_roll=payload.roll,
            english_score=payload.english_score,
            math_score=payload.math_score,
            history_score=payload.history_score,
        )
        self.student_repository.create_student(student)
        self.course_repository.add_subject_score(subject)
        self.db.commit()          # save both tables together
        self.db.refresh(student)  # to get the new id
        return self.make_response(student)

    # ---------- UPDATE ----------
    def update_student(self, roll: int, payload: StudentUpdate):
        student = self.find_student_or_404(roll)

        if payload.name is not None:
            student.name = payload.name
        if payload.email is not None:
            student.email = payload.email

        score = self.course_repository.get_course_by_roll(roll)
        if score is None:  # create a marks row if none exists
            score = Subjects(student_roll=roll, english_score=0, math_score=0, history_score=0)
            self.course_repository.add_subject_score(score)

        if payload.english_score is not None:
            score.english_score = payload.english_score
        if payload.math_score is not None:
            score.math_score = payload.math_score
        if payload.history_score is not None:
            score.history_score = payload.history_score

        self.db.commit()
        return self.make_response(student)

    # ---------- DELETE ----------
    def delete_student(self, roll: int):
        student = self.find_student_or_404(roll)
        score = self.course_repository.get_course_by_roll(roll)
        if score:
            self.course_repository.delete_subject_score(score)
        self.student_repository.delete_student(student)
        self.db.commit()
