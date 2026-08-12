# 🎓 College Database Management System

A full-stack **College Database Management System** built with **Python, Flask, PostgreSQL, SQLAlchemy, HTML, CSS, JavaScript, and Docker**.

The application provides a centralized platform for managing students, faculty, departments, courses, enrollments, and attendance.

## 🌐 Live Demo

**Live Application:** https://s4-college-database-management.onrender.com/

## 📦 GitHub Repository

**Repository:** https://github.com/sathwik-svg/s4-college-database-management

## 🚀 Features

* 👨‍🎓 Student management
* 👨‍🏫 Faculty management
* 🏢 Department management
* 📚 Course management
* 📝 Student enrollment
* 📅 Attendance management
* 📊 Dashboard statistics
* 🔍 REST API endpoints
* ✅ Input validation
* 🗄️ PostgreSQL relational database
* 🐳 Docker containerization
* ❤️ Application health monitoring
* ☁️ Render cloud deployment
* 📱 Responsive web interface

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       Browser       │
                    │   HTML/CSS/JS UI    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Flask App       │
                    │    Python Backend   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   SQLAlchemy ORM    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │   College Database  │
                    └─────────────────────┘
```

## 🛠️ Technology Stack

| Technology       | Purpose                |
| ---------------- | ---------------------- |
| Python           | Backend programming    |
| Flask            | Web framework          |
| Flask-SQLAlchemy | Database ORM           |
| PostgreSQL       | Relational database    |
| HTML5            | Web structure          |
| CSS3             | User interface         |
| JavaScript       | Dynamic frontend       |
| Docker           | Containerization       |
| Gunicorn         | Production WSGI server |
| Git              | Version control        |
| GitHub           | Source code hosting    |
| Render           | Cloud deployment       |

## 📂 Project Structure

```text
s4-college-database-management/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── render.yaml
├── .gitignore
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── tests/
    └── test_app.py
```

## 🗄️ Database Design

The system contains six main entities:

```text
Departments
     │
     ├──────── Students
     │
     ├──────── Faculty
     │
     └──────── Courses
                    │
                    ├──────── Enrollments
                    │
                    └──────── Attendance
```

### Tables

* `departments`
* `students`
* `faculty`
* `courses`
* `enrollments`
* `attendance`

The database uses primary keys, foreign keys, unique constraints, validation rules, and relational integrity.

## 🔌 REST API

### Health Check

```http
GET /health
```

### Students

```http
GET /api/students
POST /api/students
DELETE /api/students/<id>
```

### Departments

```http
GET /api/departments
```

### Faculty

```http
GET /api/faculty
POST /api/faculty
```

### Courses

```http
GET /api/courses
POST /api/courses
```

### Enrollments

```http
GET /api/enrollments
POST /api/enrollments
```

### Attendance

```http
GET /api/attendance
POST /api/attendance
```

## 💻 Run Locally

Clone the repository:

```bash
git clone https://github.com/sathwik-svg/s4-college-database-management.git
cd s4-college-database-management
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a PostgreSQL database and configure:

```text
DATABASE_URL=postgresql://username:password@localhost:5432/college_management
```

Start the application:

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

## 🐳 Run with Docker

Build the image:

```bash
docker build -t s4-college-database-management .
```

Run:

```bash
docker run --rm \
  -p 5000:5000 \
  --env-file .env \
  s4-college-database-management
```

Open:

```text
http://localhost:5000
```

## 🧪 Testing

Run:

```bash
pytest -q
```

The test suite validates:

* Application health endpoint
* Home page
* Student API
* Department API
* Course API

## ☁️ Deployment

The application is containerized with Docker and deployed on Render.

Deployment architecture:

```text
GitHub
   │
   ▼
Render Blueprint
   │
   ├── Docker Web Service
   │
   └── PostgreSQL Database
   │
   ▼
Live Application
```

Production server:

```text
Gunicorn
```

Health endpoint:

```text
/health
```

## 🔐 Environment Variables

The application uses environment variables for database configuration.

```env
DATABASE_URL=postgresql://username:password@host:5432/database
```

Sensitive credentials are not committed to GitHub.

## 📊 Learning Outcomes

This project demonstrates practical knowledge of:

* Relational database design
* SQL and PostgreSQL
* Database normalization concepts
* Primary and foreign keys
* CRUD operations
* REST API development
* Flask application architecture
* SQLAlchemy ORM
* Frontend-backend integration
* Docker containerization
* Production deployment
* Environment-based configuration
* Health checks
* Git and GitHub workflows

## 🎯 Academic Relevance

This project covers concepts from:

* Database Management Systems
* Web Application Development
* Software Engineering
* Object-Oriented Programming
* Data Management
* Cloud Computing

## 👨‍💻 Author

**Sathwik**

B.Tech Computer Science & Engineering

GitHub: https://github.com/sathwik-svg

## 📌 Project

**Semester:** 4
**Project:** S4-P1
**Repository:** `s4-college-database-management`

---

⭐ If you find this project useful, consider starring the repository.
