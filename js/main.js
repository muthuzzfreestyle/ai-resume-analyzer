function analyzeResume() {

    const fileInput = document.getElementById("resumeFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select your resume first.");
        return;
    }

    const allowedTypes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];

    if (!allowedTypes.includes(file.type)) {
        alert("Please upload a PDF or DOC/DOCX file.");
        return;
    }

    alert("Resume selected successfully: " + file.name);
}

function logout() {

    localStorage.removeItem("user");
    localStorage.removeItem("resume_id");
    localStorage.removeItem("selected_job_id");

    window.location.href = "login.html";
}
