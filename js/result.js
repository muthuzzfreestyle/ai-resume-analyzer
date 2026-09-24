const resumeId = localStorage.getItem("resume_id");

const resumeNameElement = document.getElementById("resumeName");
const targetRoleElement = document.getElementById("targetRole");

const atsScoreElement = document.getElementById("atsScore");
const skillScoreElement = document.getElementById("skillScore");
const educationScoreElement = document.getElementById("educationScore");
const experienceScoreElement = document.getElementById("experienceScore");
const formattingScoreElement = document.getElementById("formattingScore");

const skillsList = document.getElementById("skillsList");
const educationList = document.getElementById("educationList");
const experienceList = document.getElementById("experienceList");
const suggestionsList = document.getElementById("suggestions");


// =========================
// CHECK RESUME ID
// =========================

if (!resumeId) {

    alert("No resume found.");

    window.location.href = "upload.html";

}


// =========================
// ANALYZE RESUME
// =========================

async function analyzeResume() {

    try {

        const response = await fetch(
            `http://127.0.0.1:5000/api/resume/${resumeId}/analyze`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        console.log("Analysis Response:", data);

        if (!response.ok || data.status !== "success") {

            throw new Error(
                data.message || "Resume analysis failed."
            );

        }

        displayAnalysis(data);

    } catch (error) {

        console.error("Analysis Error:", error);

        alert("Unable to analyze resume.");

    }

}


// =========================
// DISPLAY ANALYSIS
// =========================

function displayAnalysis(data) {

    if (atsScoreElement) {
        atsScoreElement.textContent =
            `${data.ats_score || 0}%`;
    }

    if (skillScoreElement) {
        skillScoreElement.textContent =
            `${data.skill_score || 0}%`;
    }

    if (educationScoreElement) {
        educationScoreElement.textContent =
            `${data.education_score || 0}%`;
    }

    if (experienceScoreElement) {
        experienceScoreElement.textContent =
            `${data.experience_score || 0}%`;
    }

    if (formattingScoreElement) {
        formattingScoreElement.textContent =
            `${data.formatting_score || 0}%`;
    }


    // =========================
    // SKILLS
    // =========================

    if (skillsList) {

        skillsList.innerHTML = "";

        if (
            data.detected_skills &&
            data.detected_skills.length > 0
        ) {

            data.detected_skills.forEach(function (skill) {

                const li = document.createElement("li");

                li.textContent = skill;

                skillsList.appendChild(li);

            });

        } else {

            const li = document.createElement("li");

            li.textContent =
                "No skills detected.";

            skillsList.appendChild(li);

        }

    }


    // =========================
    // EDUCATION
    // =========================

    if (educationList) {

        educationList.innerHTML = "";

        if (
            data.education &&
            data.education.length > 0
        ) {

            data.education.forEach(function (education) {

                const li = document.createElement("li");

                li.textContent = education;

                educationList.appendChild(li);

            });

        } else {

            const li = document.createElement("li");

            li.textContent =
                "No education information detected.";

            educationList.appendChild(li);

        }

    }


    // =========================
    // EXPERIENCE
    // =========================

    if (experienceList) {

        experienceList.innerHTML = "";

        if (
            data.experience &&
            data.experience.length > 0
        ) {

            data.experience.forEach(function (experience) {

                const li = document.createElement("li");

                li.textContent = experience;

                experienceList.appendChild(li);

            });

        } else {

            const li = document.createElement("li");

            li.textContent =
                "No experience information detected.";

            experienceList.appendChild(li);

        }

    }


    // =========================
    // SUGGESTIONS
    // =========================

    if (suggestionsList) {

        suggestionsList.innerHTML = "";

        if (
            data.suggestions &&
            data.suggestions.length > 0
        ) {

            data.suggestions.forEach(function (suggestion) {

                const li = document.createElement("li");

                li.textContent = suggestion;

                suggestionsList.appendChild(li);

            });

        } else {

            const li = document.createElement("li");

            li.textContent =
                "No suggestions available.";

            suggestionsList.appendChild(li);

        }

    }

}


// =========================
// LOAD RESUME DETAILS
// =========================

async function loadResumeDetails() {

    try {

        const response = await fetch(
            `http://127.0.0.1:5000/api/resume/${resumeId}/analysis`
        );

        const data = await response.json();

        console.log("Stored Analysis:", data);

        if (
            response.ok &&
            data.status === "success"
        ) {

            const analysis = data.analysis;

            if (atsScoreElement) {
                atsScoreElement.textContent =
                    `${analysis.ats_score || 0}%`;
            }

            if (skillScoreElement) {
                skillScoreElement.textContent =
                    `${analysis.skill_score || 0}%`;
            }

            if (educationScoreElement) {
                educationScoreElement.textContent =
                    `${analysis.education_score || 0}%`;
            }

            if (experienceScoreElement) {
                experienceScoreElement.textContent =
                    `${analysis.experience_score || 0}%`;
            }

            if (formattingScoreElement) {
                formattingScoreElement.textContent =
                    `${analysis.formatting_score || 0}%`;
            }

        }

    } catch (error) {

        console.error(
            "Load Analysis Error:",
            error
        );

    }

}


// =========================
// BUTTONS
// =========================

const goToJobs =
    document.getElementById("goToJobs");

if (goToJobs) {

    goToJobs.addEventListener(
        "click",
        function () {

            window.location.href =
                "jobs.html";

        }
    );

}


const goToDashboard =
    document.getElementById("goToDashboard");

if (goToDashboard) {

    goToDashboard.addEventListener(
        "click",
        function () {

            location.href = "dashboard.html";

        }
    );

}


// =========================
// START
// =========================

analyzeResume();