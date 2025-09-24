from fastapi import FastAPI, Depends, HTTPException
from models import (
    Student,
    Teacher,
    SessionLocal,
    engine,
    Course,
    Enrollment,
    ScrapedResource,
)
from pydantic import BaseModel, Field
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import Depends


# add Pydantic models
class ScrapedResourceData(BaseModel):
    url: str
    content: str


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int
    teacher_id: int


# Pydantic models for data validation and requests
class PersonBase(BaseModel):
    name: str
    email: str


class StudentCreate(PersonBase):
    major: str


class TeacherCreate(PersonBase):
    department: str


# Creating a FastAPI instance
app = FastAPI()


# Defining a simple endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, SMS API!"}


# Creating a dependency to manage database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Creating a new student
@app.post("/students/")
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(
        name=student_data.name, email=student_data.email, major=student_data.major
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": "Student created successfully! 🎉", "student_id": db_student.id}


# Creating a new course
@app.post("/courses/")
def create_course(course_data: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(
        title=course_data.title,
        description=course_data.description,
        capacity=course_data.capacity,
        teacher_id=course_data.teacher_id,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return {"message": "Course created successfully!", "course_id": db_course.id}


# Read all courses
@app.get("/courses/")
def read_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


# Create a new teacher
@app.post("/teachers/")
def create_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = Teacher(
        name=teacher_data.name,
        email=teacher_data.email,
        department=teacher_data.department,
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return {"message": "Teacher created successfully! 🎉", "teacher_id": db_teacher.id}


# Create a new enrollment (with business rules)
@app.post("/enrollments/")
def create_enrollment(enrollment_data: EnrollmentCreate, db: Session = Depends(get_db)):
    # Business Rule 1: Check for duplicate enrollment
    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == enrollment_data.student_id,
            Enrollment.course_id == enrollment_data.course_id,
        )
        .first()
    )

    if existing_enrollment:
        # Returns a 409 Conflict error
        raise HTTPException(
            status_code=409, detail="Student is already enrolled in this course."
        )

    # Business Rule 2: Enforce course capacity
    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    current_enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.course_id == enrollment_data.course_id)
        .count()
    )
    if current_enrollments >= course.capacity:
        # Returns a 400 Bad Request error
        raise HTTPException(status_code=400, detail="Course is at full capacity.")

    # Create the new enrollment
    db_enrollment = Enrollment(
        student_id=enrollment_data.student_id, course_id=enrollment_data.course_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return {
        "message": "Enrollment created successfully!",
        "enrollment_id": db_enrollment.id,
    }


# Read all enrollments
@app.get("/enrollments/")
def read_enrollments(db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).all()
    return enrollments


# For scrapped data
@app.post("/import-data/")
def import_scraped_data(
    resources: list[ScrapedResourceData], db: Session = Depends(get_db)
):
    # Convert Pydantic models to SQLAlchemy ORM models
    db_resources = [ScrapedResource(url=r.url, content=r.content) for r in resources]

    db.add_all(db_resources)
    db.commit()

    return {"message": f"Successfully imported {len(db_resources)} scraped resources."}
