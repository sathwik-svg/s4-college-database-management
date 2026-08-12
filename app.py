import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not configured")

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql://", 1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.errorhandler(Exception)
def handle_exception(error):
    db.session.rollback()

    return jsonify({
        "status": "error",
        "error_type": type(error).__name__,
        "error": str(error)
    }), 500


db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)


class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship("Department")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )
    year = db.Column(db.Integer, nullable=False)

    department = db.relationship("Department")


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    department = db.relationship("Department")


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )
    semester = db.Column(db.String(30), nullable=False)
    grade = db.Column(db.String(5))

    student = db.relationship("Student")
    course = db.relationship("Course")


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )
    classes_attended = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    classes_held = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    student = db.relationship("Student")
    course = db.relationship("Course")

    @property
    def percentage(self):
        if self.classes_held == 0:
            return 0

        return round(
            (self.classes_attended / self.classes_held) * 100,
            2
        )


@app.route("/")
def index():
    try:
        statistics = {
            "students": Student.query.count(),
            "faculty": Faculty.query.count(),
            "departments": Department.query.count(),
            "courses": Course.query.count(),
            "enrollments": Enrollment.query.count(),
        }

        return render_template(
            "index.html",
            statistics=statistics
        )

    except Exception as error:
        return jsonify({
            "status": "error",
            "service": "college-database-management",
            "error": str(error)
        }), 500


@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.order_by(
        Student.id.desc()
    ).all()

    return jsonify([
        {
            "id": student.id,
            "roll_number": student.roll_number,
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "department": student.department.name,
            "department_id": student.department_id,
            "year": student.year
        }
        for student in students
    ])


@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json()

    required = [
        "roll_number",
        "name",
        "email",
        "department_id",
        "year"
    ]

    if not data or not all(
        field in data for field in required
    ):
        return jsonify({
            "error": "Missing required fields"
        }), 400

    if Student.query.filter_by(
        roll_number=data["roll_number"]
    ).first():
        return jsonify({
            "error": "Roll number already exists"
        }), 409

    if Student.query.filter_by(
        email=data["email"]
    ).first():
        return jsonify({
            "error": "Email already exists"
        }), 409

    department = db.session.get(
        Department,
        data["department_id"]
    )

    if not department:
        return jsonify({
            "error": "Department not found"
        }), 404

    year = int(data["year"])

    if year not in range(1, 5):
        return jsonify({
            "error": "Year must be between 1 and 4"
        }), 400

    student = Student(
        roll_number=data["roll_number"],
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        department_id=data["department_id"],
        year=year
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "id": student.id
    }), 201


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = db.session.get(Student, student_id)

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    })


@app.route("/api/departments", methods=["GET"])
def get_departments():
    departments = Department.query.order_by(
        Department.name
    ).all()

    return jsonify([
        {
            "id": department.id,
            "name": department.name,
            "code": department.code
        }
        for department in departments
    ])


@app.route("/api/faculty", methods=["GET"])
def get_faculty():
    faculty = Faculty.query.order_by(
        Faculty.name
    ).all()

    return jsonify([
        {
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "department": member.department.name,
            "department_id": member.department_id
        }
        for member in faculty
    ])



@app.route("/api/faculty", methods=["POST"])
def create_faculty():
    data = request.get_json() or {}

    required = ["name", "email", "department_id"]

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    if Faculty.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Faculty email already exists"}), 409

    department = db.session.get(
        Department,
        data["department_id"]
    )

    if not department:
        return jsonify({"error": "Department not found"}), 404

    member = Faculty(
        name=data["name"],
        email=data["email"],
        department_id=data["department_id"]
    )

    db.session.add(member)
    db.session.commit()

    return jsonify({
        "message": "Faculty created successfully",
        "id": member.id
    }), 201


@app.route("/api/courses", methods=["POST"])
def create_course():
    data = request.get_json() or {}

    required = [
        "name",
        "code",
        "credits",
        "department_id"
    ]

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    if Course.query.filter_by(code=data["code"]).first():
        return jsonify({"error": "Course code already exists"}), 409

    department = db.session.get(
        Department,
        data["department_id"]
    )

    if not department:
        return jsonify({"error": "Department not found"}), 404

    credits = int(data["credits"])

    if credits < 1 or credits > 10:
        return jsonify({"error": "Credits must be between 1 and 10"}), 400

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=credits,
        department_id=data["department_id"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "id": course.id
    }), 201


@app.route("/api/enrollments", methods=["POST"])
def create_enrollment():
    data = request.get_json() or {}

    required = [
        "student_id",
        "course_id",
        "semester"
    ]

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    student = db.session.get(
        Student,
        data["student_id"]
    )

    course = db.session.get(
        Course,
        data["course_id"]
    )

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if not course:
        return jsonify({"error": "Course not found"}), 404

    existing = Enrollment.query.filter_by(
        student_id=data["student_id"],
        course_id=data["course_id"],
        semester=data["semester"]
    ).first()

    if existing:
        return jsonify({
            "error": "Student is already enrolled in this course for this semester"
        }), 409

    enrollment = Enrollment(
        student_id=data["student_id"],
        course_id=data["course_id"],
        semester=data["semester"],
        grade=data.get("grade")
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Enrollment created successfully",
        "id": enrollment.id
    }), 201


@app.route("/api/attendance", methods=["POST"])
def create_attendance():
    data = request.get_json() or {}

    required = [
        "student_id",
        "course_id",
        "classes_attended",
        "classes_held"
    ]

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    student = db.session.get(
        Student,
        data["student_id"]
    )

    course = db.session.get(
        Course,
        data["course_id"]
    )

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if not course:
        return jsonify({"error": "Course not found"}), 404

    attended = int(data["classes_attended"])
    held = int(data["classes_held"])

    if attended < 0 or held < 0:
        return jsonify({
            "error": "Attendance values cannot be negative"
        }), 400

    if attended > held:
        return jsonify({
            "error": "Classes attended cannot exceed classes held"
        }), 400

    record = Attendance.query.filter_by(
        student_id=data["student_id"],
        course_id=data["course_id"]
    ).first()

    if record:
        record.classes_attended = attended
        record.classes_held = held
    else:
        record = Attendance(
            student_id=data["student_id"],
            course_id=data["course_id"],
            classes_attended=attended,
            classes_held=held
        )
        db.session.add(record)

    db.session.commit()

    return jsonify({
        "message": "Attendance saved successfully",
        "id": record.id,
        "percentage": record.percentage
    }), 201


@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = Course.query.order_by(
        Course.name
    ).all()

    return jsonify([
        {
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "credits": course.credits,
            "department": course.department.name,
            "department_id": course.department_id
        }
        for course in courses
    ])


@app.route("/api/enrollments", methods=["GET"])
def get_enrollments():
    enrollments = Enrollment.query.order_by(
        Enrollment.id.desc()
    ).all()

    return jsonify([
        {
            "id": enrollment.id,
            "student": enrollment.student.name,
            "roll_number": enrollment.student.roll_number,
            "course": enrollment.course.name,
            "course_code": enrollment.course.code,
            "semester": enrollment.semester,
            "grade": enrollment.grade
        }
        for enrollment in enrollments
    ])


@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    records = Attendance.query.order_by(
        Attendance.id.desc()
    ).all()

    return jsonify([
        {
            "id": record.id,
            "student": record.student.name,
            "course": record.course.name,
            "classes_attended": record.classes_attended,
            "classes_held": record.classes_held,
            "percentage": record.percentage
        }
        for record in records
    ])


@app.route("/health")
def health():
    try:
        db.session.execute(
            db.text("SELECT 1")
        )

        return jsonify({
            "status": "healthy",
            "database": "connected",
            "service": "college-database-management"
        })

    except Exception:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "service": "college-database-management"
        }), 503


    
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )
