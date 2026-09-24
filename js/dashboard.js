const user = JSON.parse(
    localStorage.getItem("user") || "null"
);

const resumeId =
    localStorage.getItem("resume_id");


// =========================
// CHECK LOGIN
// =========================

if (!user) {

    window.location.href = "login.html";

}


// =========================
// USER NAME
// =========================

const userName =
    document.getElementById("userName");

if (userName && user) {

    userName.textContent =
        user.name || "User";

}


// =========================
// LOAD DASHBOARD DATA
// =========================

async function loadDashboard() {

    if (!resumeId) {
        return;
    }

    try {

        const response = await fetch(
            `http://127.0.0.1:5000/api/resume/${resumeId}/analysis`
        );

        const data = await response.json();

        console.log(
            "Dashboard Analysis:",
            data
        );

        if (
            !response.ok ||
            data.status !== "success"
        ) {
            return;
        }

        const analysis =
            data.analysis;

        const atsScore =
            document.getElementById("atsScore");

        const skillScore =
            document.getElementById("skillScore");

        const educationScore =
            document.getElementById(
                "educationScore"
            );

        const experienceScore =
            document.getElementById(
                "experienceScore"
            );

        const formattingScore =
            document.getElementById(
                "formattingScore"
            );


        if (atsScore) {

            atsScore.textContent =
                `${analysis.ats_score || 0}%`;

        }


        if (skillScore) {

            skillScore.textContent =
                `${analysis.skill_score || 0}%`;

        }


        if (educationScore) {

            educationScore.textContent =
                `${analysis.education_score || 0}%`;

        }


        if (experienceScore) {

            experienceScore.textContent =
                `${analysis.experience_score || 0}%`;

        }


        if (formattingScore) {

            formattingScore.textContent =
                `${analysis.formatting_score || 0}%`;

        }

    } catch (error) {

        console.error(
            "Dashboard Error:",
            error
        );

    }

}


// =========================
// UPLOAD BUTTON
// =========================

const goToUpload =
    document.getElementById("goToUpload");

if (goToUpload) {

    goToUpload.addEventListener(
        "click",
        function () {

            window.location.href =
                "upload.html";

        }
    );

}


// =========================
// ANALYSIS BUTTON
// =========================

const goToAnalysis =
    document.getElementById("goToAnalysis");

if (goToAnalysis) {

    goToAnalysis.addEventListener(
        "click",
        function () {

            if (!resumeId) {

                window.location.href =
                    "upload.html";

                return;

            }

            window.location.href =
                "result.html";

        }
    );

}


// =========================
// JOBS BUTTON
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


// =========================
// LOAD
// =========================

loadDashboard();