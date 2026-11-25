// ==========================================
// script.js  ->  Calls the backend API from the frontend
// ==========================================

// Address of the backend
const API_URL = "http://127.0.0.1:8000/students";

// Remembers which roll is being edited (null means adding a new student)
let editingRoll = null;


// ---------- 1. Load all students and show them in the table (GET) ----------
async function loadStudents() {
    const response = await fetch(API_URL);
    const students = await response.json();

    const table = document.getElementById("student-table");
    table.innerHTML = "";   // clear the old rows

    // Show the total number of students
    document.getElementById("total").innerText = students.length + " students";

    // No students yet
    if (students.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="11" class="text-center text-muted py-4">
                    No students yet. Add one using the form above.
                </td>
            </tr>
        `;
        return;
    }

    for (const s of students) {
        table.innerHTML += `
            <tr>
                <td>${s.roll}</td>
                <td>${s.name}</td>
                <td>${s.age}</td>
                <td>${s.email}</td>
                <td>${s.session}</td>
                <td>${s.english_score}</td>
                <td>${s.math_score}</td>
                <td>${s.history_score}</td>
                <td><strong>${s.average}</strong></td>
                <td><span class="badge ${getBadgeColor(s.comment)}">${s.comment}</span></td>
                <td class="text-nowrap">
                    <button class="btn btn-warning btn-sm" onclick="editStudent(${s.roll})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteStudent(${s.roll})">Delete</button>
                </td>
            </tr>
        `;
    }
}


// ---------- 2. Form submit -> Add (POST) or Update (PATCH) ----------
document.getElementById("student-form").addEventListener("submit", async function (event) {
    event.preventDefault();   // stop the page from reloading

    // Build an object from the form data
    const data = {
        name: document.getElementById("name").value,
        age: Number(document.getElementById("age").value),
        email: document.getElementById("email").value,
        roll: Number(document.getElementById("roll").value),
        session: document.getElementById("session").value,
        english_score: Number(document.getElementById("english").value),
        math_score: Number(document.getElementById("math").value),
        history_score: Number(document.getElementById("history").value),
    };

    let response;
    if (editingRoll === null) {
        // New student
        response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
    } else {
        // Update existing student
        response = await fetch(`${API_URL}/${editingRoll}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
    }

    if (response.ok) {
        showMessage(editingRoll === null ? "Student added!" : "Student updated!", "success");
        resetForm();
        loadStudents();
    } else {
        const error = await response.json();
        showMessage("Error: " + getErrorText(error), "danger");
    }
});


// ---------- 3. Edit button -> fill the form with the student's data ----------
async function editStudent(roll) {
    const response = await fetch(`${API_URL}/${roll}`);
    const s = await response.json();

    document.getElementById("name").value = s.name;
    document.getElementById("age").value = s.age;
    document.getElementById("email").value = s.email;
    document.getElementById("roll").value = s.roll;
    document.getElementById("session").value = s.session;
    document.getElementById("english").value = s.english_score;
    document.getElementById("math").value = s.math_score;
    document.getElementById("history").value = s.history_score;

    // Roll, age and session can't be updated (the API only changes name, email and marks)
    document.getElementById("roll").disabled = true;
    document.getElementById("age").disabled = true;
    document.getElementById("session").disabled = true;

    editingRoll = roll;
    document.getElementById("form-title").innerText = "Edit Student (Roll " + roll + ")";
    document.getElementById("submit-btn").innerText = "Update Student";
    document.getElementById("submit-btn").className = "btn btn-success";
    document.getElementById("cancel-btn").classList.remove("d-none");

    window.scrollTo({ top: 0, behavior: "smooth" });   // scroll up to the form
}


// ---------- 4. Delete (DELETE) ----------
async function deleteStudent(roll) {
    if (!confirm("Delete student with roll " + roll + "?")) return;

    const response = await fetch(`${API_URL}/${roll}`, { method: "DELETE" });

    if (response.ok) {
        showMessage("Student deleted!", "success");
        loadStudents();
    } else {
        const error = await response.json();
        showMessage("Error: " + getErrorText(error), "danger");
    }
}


// ---------- Small helper functions ----------

// Clear the form and go back to "Add" mode
function resetForm() {
    document.getElementById("student-form").reset();
    document.getElementById("roll").disabled = false;
    document.getElementById("age").disabled = false;
    document.getElementById("session").disabled = false;
    editingRoll = null;
    document.getElementById("form-title").innerText = "Add New Student";
    document.getElementById("submit-btn").innerText = "Add Student";
    document.getElementById("submit-btn").className = "btn btn-primary";
    document.getElementById("cancel-btn").classList.add("d-none");
}

// Show a Bootstrap alert at the top. type = "success" (green) or "danger" (red)
function showMessage(text, type) {
    const message = document.getElementById("message");
    message.innerText = text;
    message.className = "alert alert-" + type;

    // Hide the message after 3 seconds
    setTimeout(() => message.classList.add("d-none"), 3000);
}

// Pick a badge color for each comment
function getBadgeColor(comment) {
    if (comment === "Excellent") return "bg-success";
    if (comment === "Very Good") return "bg-primary";
    if (comment === "Good") return "bg-info text-dark";
    return "bg-danger";   // Need Improvement
}

// Turn a FastAPI error into simple text
function getErrorText(error) {
    if (typeof error.detail === "string") return error.detail;
    // For validation errors (e.g. age = 40)
    return error.detail.map(e => e.loc[e.loc.length - 1] + ": " + e.msg).join(", ");
}


// Load the student list as soon as the page opens
loadStudents();
