# ==========================================
# Router / Controller  ->  The API URLs
# ==========================================
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from service.student_service import StudentService
from utils.schema import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/students", tags=["Student"])


# GET /students  ->  get all students
@router.get("", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return StudentService(db).get_students()


# GET /students/5  ->  get the student with roll 5
@router.get("/{roll}", response_model=StudentResponse)
def get_one_student(roll: int, db: Session = Depends(get_db)):
    return StudentService(db).get_student(roll)


# POST /students  ->  add a new student
@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def add_student(payload: StudentCreate, db: Session = Depends(get_db)):
    return StudentService(db).add_student(payload)


# PATCH /students/5  ->  update the student with roll 5
@router.patch("/{roll}", response_model=StudentResponse)
def update_student(roll: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    return StudentService(db).update_student(roll, payload)


# DELETE /students/5  ->  delete the student with roll 5
@router.delete("/{roll}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(roll: int, db: Session = Depends(get_db)):
    StudentService(db).delete_student(roll)
