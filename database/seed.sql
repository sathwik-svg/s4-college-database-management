INSERT INTO departments (name, code)
VALUES
    ('Computer Science and Engineering', 'CSE'),
    ('Electronics and Communication Engineering', 'ECE'),
    ('Mechanical Engineering', 'MECH'),
    ('Civil Engineering', 'CIVIL')
ON CONFLICT DO NOTHING;

INSERT INTO faculty (name, email, department_id)
SELECT 'Dr. Ravi Kumar', 'ravi.cse@college.edu', id
FROM departments
WHERE code = 'CSE'
ON CONFLICT DO NOTHING;

INSERT INTO faculty (name, email, department_id)
SELECT 'Dr. Priya Sharma', 'priya.ece@college.edu', id
FROM departments
WHERE code = 'ECE'
ON CONFLICT DO NOTHING;

INSERT INTO students
    (roll_number, name, email, phone, department_id, year)
SELECT
    'CSE001',
    'Arjun Kumar',
    'arjun@example.com',
    '9876543210',
    id,
    2
FROM departments
WHERE code = 'CSE'
ON CONFLICT DO NOTHING;

INSERT INTO students
    (roll_number, name, email, phone, department_id, year)
SELECT
    'CSE002',
    'Rahul Sharma',
    'rahul@example.com',
    '9876543211',
    id,
    2
FROM departments
WHERE code = 'CSE'
ON CONFLICT DO NOTHING;

INSERT INTO courses (name, code, credits, department_id)
SELECT
    'Database Management Systems',
    'CS301',
    4,
    id
FROM departments
WHERE code = 'CSE'
ON CONFLICT DO NOTHING;

INSERT INTO courses (name, code, credits, department_id)
SELECT
    'Operating Systems',
    'CS302',
    4,
    id
FROM departments
WHERE code = 'CSE'
ON CONFLICT DO NOTHING;
