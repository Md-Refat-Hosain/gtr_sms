# test_main.py
import pytest
from conftest import client  # Import the TestClient fixture


# --- Test 1: Enrollment Rule (Course Capacity) ---
def test_enrollment_capacity(client, db_session):
    # Setup: Create Teacher and Course (capacity 1)
    teacher_resp = client.post(
        "/teachers/",
        json={"name": "T1", "email": "t1@school.com", "department": "Science"},
    )
    course_resp = client.post(
        "/courses/",
        json={
            "title": "Math 101",
            "capacity": 1,
            "teacher_id": teacher_resp.json()["teacher_id"],
        },
    )
    course_id = course_resp.json()["course_id"]

    # Setup: Create two students
    student1_resp = client.post(
        "/students/", json={"name": "S1", "email": "s1@school.com", "major": "Physics"}
    )
    student1_id = student1_resp.json()["student_id"]
    student2_resp = client.post(
        "/students/",
        json={"name": "S2", "email": "s2@school.com", "major": "Chemistry"},
    )
    student2_id = student2_resp.json()["student_id"]

    # Action 1: Enroll Student 1 (Should succeed - Status 200)
    enroll_success_resp = client.post(
        "/enrollments/", json={"student_id": student1_id, "course_id": course_id}
    )
    assert enroll_success_resp.status_code == 200

    # Action 2: Enroll Student 2 (Should fail - Capacity full)
    enroll_fail_resp = client.post(
        "/enrollments/", json={"student_id": student2_id, "course_id": course_id}
    )

    # Assertion: Check for the 400 Bad Request error
    assert enroll_fail_resp.status_code == 400
    assert "full capacity" in enroll_fail_resp.json()["detail"]


# --- Test 2: Scraper Parsing/Import Endpoint ---
def test_import_scraped_data(client, db_session):
    # Sample data to simulate scraped resources
    scraped_data = [
        {"url": "http://example.com/r1", "content": "Resource 1 content"},
        {"url": "http://example.com/r2", "content": "Resource 2 content"},
    ]

    # Action: Post the data to the import endpoint
    import_resp = client.post("/import-data/", json=scraped_data)

    # Assertion 1: Check for successful creation status
    assert import_resp.status_code == 200

    # Assertion 2: Check the response message
    assert "Successfully imported 2 scraped resources" in import_resp.json()["message"]
