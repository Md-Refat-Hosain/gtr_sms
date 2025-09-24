# School Management System (SMS) API

A backend service built with **FastAPI** and **SQLAlchemy** to manage students, teachers, courses, and enrollments, while demonstrating core Object-Oriented Programming (OOP) principles.

## Prerequisites

* Python 3.11+
* PostgreSQL Database

## Setup and Installation

1.  **Clone the Repository/create the project folder :**
    ```bash
    git clone [[Your Repository URL](https://github.com/Md-Refat-Hosain/gtr_sms)]
    cd sms_api
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install "fastapi[standard]" sqlalchemy psycopg2-binary python-dotenv pytest pytest-asyncio httpx
    ```

4.  **Database Configuration:**
    Create a file named **`.env`** in the project root and add your database credentials:
    ```dotenv
    # .env file content
    DATABASE_URL="postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]"
    # Example: DATABASE_URL="postgresql://postgres:mohdrifat462@localhost:5432/GTR_WEB_SQL"
    ```

5.  **Initialize Database Tables:**
    Run the `models.py` script once to create all the necessary tables (`students`, `teachers`, `courses`, `enrollments`, `scraped_resources`).
    ```bash
    python models.py
    ```

## Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
