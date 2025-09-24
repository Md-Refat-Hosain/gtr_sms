### 2. `DESIGN.md` (OOP Pillars Explanation)

This file explains where you implemented the four core OOP pillars as required.

```markdown
# DESIGN.md: Object-Oriented Programming (OOP) Pillars

The School Management System API is designed to demonstrate the four pillars of OOP through its data models and API logic.

## 1. Abstraction & Inheritance

* **Abstraction:** The **`Person`** class in `models.py` serves as an abstract base for all individuals in the system. It contains common attributes like `id`, `name`, and `email`, abstracting away the specifics of whether an individual is a student or a teacher.

* **Inheritance:** The **`Student`** and **`Teacher`** models inherit directly from the **`Person`** class, reusing its core attributes and extending them with specialized fields (`major` for Student, `department` for Teacher). This avoids redundant code.

## 2. Encapsulation

* **Data Validation:** **Pydantic models** are used to strictly define the input data schemas for all API endpoints, ensuring data integrity before it reaches the database layer.
* **Business Rules:** Complex logic is encapsulated within specific API functions. The `POST /enrollments` endpoint contains the logic to:
    1.  Check if a student is **already enrolled** (preventing duplicates).
    2.  Check if a course has reached its **`capacity`** (enforcing constraints).

## 3. Polymorphism

* **Structural Polymorphism:** The API endpoints demonstrate polymorphism by handling different but related data types in similar ways. For example, the `POST /students` and `POST /teachers` endpoints both perform the same base operation (creating a new **`Person`** entry in the shared `people` table) but handle two distinct data structures (`StudentCreate` and `TeacherCreate`). The API's use of Pydantic and SQLAlchemy's inheritance scheme allows the system to treat these different types uniformly when necessary.
