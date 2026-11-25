// Backend API address
const API_URL = "http://127.0.0.1:8000/students";

// null = adding a new student, a number = editing that roll
let editingRoll = null;


// 1. Show all students in the table (GET)
async function loadStudents() {
    const response = await fetch(API_URL);
    const students = await response.json();

    let rows = "";
    for (const s of students) {
        rows += `
            <tr>
                <td>${s.roll}</td>
                <td>${s.name}</td>
                <td>${s.age}</td>
                <td>${s.email}</td>
                <td>${s.session}</td>
                <td>${s.english_score}</td>
                <td>${s.math_score}</td>
                <td>${s.history_score}</td>
                <td>${s.average}</td>
                <td>${s.comment}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editStudent(${s.roll})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteStudent(${s.roll})">Delete</button>
                </td>
            </tr>
        `;
    }
    document.getElementById("student-table").innerHTML = rows;
}


// 2. Save button: add a new student (POST) or update one (PATCH)
document.getElementById("student-form").addEventListener("submit", async function (event) {
    event.preventDefault();   // stop the page from reloading

    const student = {
        name: document.getElementById("name").value,
        age: Number(document.getElementById("age").value),
        email: document.getElementById("email").value,
        roll: Number(document.getElementById("roll").value),
        session: document.getElementById("session").value,
        english_score: Number(document.getElementById("english").value),
        math_score: Number(document.getElementById("math").value),
        history_score: Number(document.getElementById("history").value),
    };

    let url = API_URL;
    let method = "POST";

    if (editingRoll !== null) {
        url = API_URL + "/" + editingRoll;
        method = "PATCH";
    }

    const response = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(student),
    });

    if (response.ok) {
        alert("Saved!");
        document.getElementById("student-form").reset();   // clear the form
        editingRoll = null;
        document.getElementById("form-title").innerText = "Add Student";
        loadStudents();
    } else {
        const error = await response.json();
        alert("Error: " + JSON.stringify(error.detail));
    }
});


// 3. Edit button: put the student's data into the form
async function editStudent(roll) {
    const response = await fetch(API_URL + "/" + roll);
    const s = await response.json();

    document.getElementById("name").value = s.name;
    document.getElementById("age").value = s.age;
    document.getElementById("email").value = s.email;
    document.getElementById("roll").value = s.roll;
    document.getElementById("session").value = s.session;
    document.getElementById("english").value = s.english_score;
    document.getElementById("math").value = s.math_score;
    document.getElementById("history").value = s.history_score;

    editingRoll = roll;
    document.getElementById("form-title").innerText = "Edit Student (Roll " + roll + ")";
}


// 4. Delete button (DELETE)
async function deleteStudent(roll) {
    if (!confirm("Delete this student?")) return;

    await fetch(API_URL + "/" + roll, { method: "DELETE" });
    loadStudents();
}


// Show the students when the page opens
loadStudents();
