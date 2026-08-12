let departments = [];
let students = [];
let courses = [];

async function api(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json"
        },
        ...options
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Request failed");
    }

    return data;
}


function openModal(id) {
    document.getElementById(id).classList.add("active");
}


function closeModal(id) {
    document.getElementById(id).classList.remove("active");
}


async function loadDepartments() {
    departments = await api("/api/departments");

    const containers = [
        "studentDepartment",
        "facultyDepartment",
        "courseDepartment"
    ];

    containers.forEach(id => {
        const select = document.getElementById(id);

        select.innerHTML = `
            <option value="">Select Department</option>
        `;

        departments.forEach(department => {
            select.innerHTML += `
                <option value="${department.id}">
                    ${department.code} - ${department.name}
                </option>
            `;
        });
    });

    const cards = document.getElementById("departmentCards");

    cards.innerHTML = departments.map(department => `
        <div class="module">
            <h3>${department.code}</h3>
            <p>${department.name}</p>
        </div>
    `).join("");
}


async function loadStudents() {
    students = await api("/api/students");

    const table = document.getElementById("studentsTable");

    if (!students.length) {
        table.innerHTML = `
            <tr>
                <td colspan="7">No students found.</td>
            </tr>
        `;
        return;
    }

    table.innerHTML = students.map(student => `
        <tr>
            <td>${student.id}</td>
            <td>${student.roll_number}</td>
            <td>${student.name}</td>
            <td>${student.email}</td>
            <td>${student.department}</td>
            <td>${student.year}</td>
            <td>
                <button
                    class="danger"
                    onclick="deleteStudent(${student.id})">
                    Delete
                </button>
            </td>
        </tr>
    `).join("");

    document.getElementById("studentCount").textContent =
        students.length;

    const select = document.getElementById("enrollmentStudent");

    select.innerHTML = `
        <option value="">Select Student</option>
    `;

    students.forEach(student => {
        select.innerHTML += `
            <option value="${student.id}">
                ${student.roll_number} - ${student.name}
            </option>
        `;
    });
}


async function loadFaculty() {
    const faculty = await api("/api/faculty");

    const table = document.getElementById("facultyTable");

    if (!faculty.length) {
        table.innerHTML = `
            <tr>
                <td colspan="4">No faculty found.</td>
            </tr>
        `;
        return;
    }

    table.innerHTML = faculty.map(member => `
        <tr>
            <td>${member.id}</td>
            <td>${member.name}</td>
            <td>${member.email}</td>
            <td>${member.department}</td>
        </tr>
    `).join("");

    document.getElementById("facultyCount").textContent =
        faculty.length;
}


async function loadCourses() {
    courses = await api("/api/courses");

    const table = document.getElementById("coursesTable");

    if (!courses.length) {
        table.innerHTML = `
            <tr>
                <td colspan="5">No courses found.</td>
            </tr>
        `;
        return;
    }

    table.innerHTML = courses.map(course => `
        <tr>
            <td>${course.id}</td>
            <td>${course.code}</td>
            <td>${course.name}</td>
            <td>${course.credits}</td>
            <td>${course.department}</td>
        </tr>
    `).join("");

    document.getElementById("courseCount").textContent =
        courses.length;

    const select = document.getElementById("enrollmentCourse");

    select.innerHTML = `
        <option value="">Select Course</option>
    `;

    courses.forEach(course => {
        select.innerHTML += `
            <option value="${course.id}">
                ${course.code} - ${course.name}
            </option>
        `;
    });
}


async function loadEnrollments() {
    const enrollments = await api("/api/enrollments");

    const table = document.getElementById("enrollmentsTable");

    if (!enrollments.length) {
        table.innerHTML = `
            <tr>
                <td colspan="6">No enrollments found.</td>
            </tr>
        `;
        return;
    }

    table.innerHTML = enrollments.map(enrollment => `
        <tr>
            <td>${enrollment.id}</td>
            <td>${enrollment.student}</td>
            <td>${enrollment.roll_number}</td>
            <td>${enrollment.course}</td>
            <td>${enrollment.semester}</td>
            <td>${enrollment.grade || "-"}</td>
        </tr>
    `).join("");

    document.getElementById("enrollmentCount").textContent =
        enrollments.length;
}


async function loadAttendance() {
    const records = await api("/api/attendance");

    const table = document.getElementById("attendanceTable");

    if (!records.length) {
        table.innerHTML = `
            <tr>
                <td colspan="5">No attendance records found.</td>
            </tr>
        `;
        return;
    }

    table.innerHTML = records.map(record => `
        <tr>
            <td>${record.student}</td>
            <td>${record.course}</td>
            <td>${record.classes_attended}</td>
            <td>${record.classes_held}</td>
            <td>${record.percentage}%</td>
        </tr>
    `).join("");
}


async function deleteStudent(id) {
    if (!confirm("Delete this student?")) {
        return;
    }

    try {
        await api(`/api/students/${id}`, {
            method: "DELETE"
        });

        await loadStudents();

        alert("Student deleted successfully.");

    } catch (error) {
        alert(error.message);
    }
}


document.getElementById("studentForm").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        try {
            await api("/api/students", {
                method: "POST",
                body: JSON.stringify({
                    roll_number:
                        document.getElementById("studentRoll").value,

                    name:
                        document.getElementById("studentName").value,

                    email:
                        document.getElementById("studentEmail").value,

                    phone:
                        document.getElementById("studentPhone").value,

                    department_id:
                        Number(
                            document.getElementById(
                                "studentDepartment"
                            ).value
                        ),

                    year:
                        Number(
                            document.getElementById(
                                "studentYear"
                            ).value
                        )
                })
            });

            event.target.reset();

            closeModal("studentModal");

            await loadStudents();

            location.reload();

        } catch (error) {
            alert(error.message);
        }
    }
);


async function init() {
    try {
        await loadDepartments();
        await loadStudents();
        await loadFaculty();
        await loadCourses();
        await loadEnrollments();
        await loadAttendance();
    } catch (error) {
        console.error(error);
    }
}


document.addEventListener("DOMContentLoaded", init);


window.onclick = event => {
    if (event.target.classList.contains("modal")) {
        event.target.classList.remove("active");
    }
};

document.getElementById("facultyForm").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        try {
            await api("/api/faculty", {
                method: "POST",
                body: JSON.stringify({
                    name: document.getElementById("facultyName").value,
                    email: document.getElementById("facultyEmail").value,
                    department_id: Number(
                        document.getElementById("facultyDepartment").value
                    )
                })
            });

            event.target.reset();
            closeModal("facultyModal");
            await loadFaculty();

            alert("Faculty created successfully.");

        } catch (error) {
            alert(error.message);
        }
    }
);


document.getElementById("courseForm").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        try {
            await api("/api/courses", {
                method: "POST",
                body: JSON.stringify({
                    name: document.getElementById("courseName").value,
                    code: document.getElementById("courseCode").value,
                    credits: Number(
                        document.getElementById("courseCredits").value
                    ),
                    department_id: Number(
                        document.getElementById("courseDepartment").value
                    )
                })
            });

            event.target.reset();
            closeModal("courseModal");
            await loadCourses();

            alert("Course created successfully.");

        } catch (error) {
            alert(error.message);
        }
    }
);


document.getElementById("enrollmentForm").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        try {
            await api("/api/enrollments", {
                method: "POST",
                body: JSON.stringify({
                    student_id: Number(
                        document.getElementById("enrollmentStudent").value
                    ),
                    course_id: Number(
                        document.getElementById("enrollmentCourse").value
                    ),
                    semester:
                        document.getElementById("enrollmentSemester").value,
                    grade:
                        document.getElementById("enrollmentGrade").value
                })
            });

            event.target.reset();
            closeModal("enrollmentModal");
            await loadEnrollments();

            alert("Enrollment created successfully.");

        } catch (error) {
            alert(error.message);
        }
    }
);


document.getElementById("attendanceForm").addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        try {
            await api("/api/attendance", {
                method: "POST",
                body: JSON.stringify({
                    student_id: Number(
                        document.getElementById("attendanceStudent").value
                    ),
                    course_id: Number(
                        document.getElementById("attendanceCourse").value
                    ),
                    classes_attended: Number(
                        document.getElementById("classesAttended").value
                    ),
                    classes_held: Number(
                        document.getElementById("classesHeld").value
                    )
                })
            });

            event.target.reset();
            closeModal("attendanceModal");
            await loadAttendance();

            alert("Attendance saved successfully.");

        } catch (error) {
            alert(error.message);
        }
    }
);


async function populateAttendanceSelectors() {
    const studentSelect =
        document.getElementById("attendanceStudent");

    const courseSelect =
        document.getElementById("attendanceCourse");

    studentSelect.innerHTML =
        '<option value="">Select Student</option>';

    courseSelect.innerHTML =
        '<option value="">Select Course</option>';

    students.forEach(student => {
        studentSelect.innerHTML += `
            <option value="${student.id}">
                ${student.roll_number} - ${student.name}
            </option>
        `;
    });

    courses.forEach(course => {
        courseSelect.innerHTML += `
            <option value="${course.id}">
                ${course.code} - ${course.name}
            </option>
        `;
    });
}


const originalInit = init;

init = async function() {
    try {
        await loadDepartments();
        await loadStudents();
        await loadFaculty();
        await loadCourses();
        await loadEnrollments();
        await loadAttendance();
        await populateAttendanceSelectors();
    } catch (error) {
        console.error(error);
    }
};
