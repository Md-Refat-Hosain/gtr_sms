from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    UniqueConstraint,
)
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker
from sqlalchemy import create_engine


#  database URL
DATABASE_URL = "postgresql://postgres:mohdrifat462@localhost:5432/GTR_WEB_SQL"

####
# Load Environment Variables
load_dotenv()
# Get the full URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if the URL was loaded (important for safety)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables or .env file.")

engine = create_engine(DATABASE_URL)
####


engine = create_engine(DATABASE_URL)

# Base class for all models
Base = declarative_base()


# Person is an abstract base class. " Abstraction "
class Person(Base):
    __tablename__ = "people"
    
    __mapper_args__ = {"polymorphic_on": "type"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    type = Column(String)

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', email='{self.email}')>"


# Student inherits from Person. " Inheritance "
class Student(Person):
    __tablename__ = "students"
    __mapper_args__ = {"polymorphic_identity": "student"}

    id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    major = Column(String)

    enrollments = relationship("Enrollment", back_populates="student")


# Teacher inherits from Person. " Inheritance "
class Teacher(Person):
    __tablename__ = "teachers"
    __mapper_args__ = {"polymorphic_identity": "teacher"}

    id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    department = Column(String)

    courses_taught = relationship("Course", back_populates="teacher")


# Course Model
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    capacity = Column(Integer)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="courses_taught")

    enrollments = relationship("Enrollment", back_populates="course")


# Enrollment is a link table for the many-to-many relationship
# between students and courses.
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="_student_course_uc"),
    )


# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully! ✅")


#
class ScrapedResource(Base):
    __tablename__ = "scraped_resources_from_FastAPI"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    content = Column(String)  


if __name__ == "__main__":
    create_tables()
