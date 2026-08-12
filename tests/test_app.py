import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code in (200, 503)


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_students_api():
    client = app.test_client()

    response = client.get("/api/students")

    assert response.status_code == 200


def test_departments_api():
    client = app.test_client()

    response = client.get("/api/departments")

    assert response.status_code == 200


def test_courses_api():
    client = app.test_client()

    response = client.get("/api/courses")

    assert response.status_code == 200
