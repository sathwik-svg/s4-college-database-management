CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS faculty (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    department_id INTEGER NOT NULL REFERENCES departments(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    roll_number VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20),
    department_id INTEGER NOT NULL REFERENCES departments(id)
        ON DELETE CASCADE,
    year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 4)
);

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(30) NOT NULL UNIQUE,
    credits INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 10),
    department_id INTEGER NOT NULL REFERENCES departments(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id)
        ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id)
        ON DELETE CASCADE,
    semester VARCHAR(30) NOT NULL,
    grade VARCHAR(5),
    UNIQUE(student_id, course_id, semester)
);

CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id)
        ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id)
        ON DELETE CASCADE,
    classes_attended INTEGER NOT NULL DEFAULT 0,
    classes_held INTEGER NOT NULL DEFAULT 0,
    CHECK (classes_attended >= 0),
    CHECK (classes_held >= 0),
    CHECK (classes_attended <= classes_held),
    UNIQUE(student_id, course_id)
);
