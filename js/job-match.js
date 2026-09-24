const resumeId =
    localStorage.getItem("resume_id");

const jobId =
    localStorage.getItem("selected_job_id");

const jobInfo =
    document.getElementById("jobInfo");

const matchScore =
    document.getElementById("matchScore");

const matchedSkills =
    document.getElementById("matchedSkills");

const missingSkills =
    document.getElementById("missingSkills");


// =========================
// CHECK DATA
// =========================

if (!resumeId || !jobId) {

    alert("Resume or job information not found.");

    window.location.href = "jobs.html";

}


// =========================
// LOAD JOB MATCH
// =========================

async function loadJobMatch() {

    try {

        const response = await fetch(
            `http://127.0.0.1:5000/api/resume/${resumeId}/jobs/${jobId}/match`
        );

        const data = await response.json();

        console.log(
            "Job Match Response:",
            data
        );

        if (
            !response.ok ||
            data.status !== "success"
        ) {

            throw new Error(
                data.message || "Job matching failed."
            );

        }

        displayJobMatch(data);

    } catch (error) {

        console.error(
            "Job Match Error:",
            error
        );

        if (jobInfo) {

            jobInfo.innerHTML =
                "<p>Unable to load job match.</p>";

        }

    }

}


// =========================
// DISPLAY JOB MATCH
// =========================

function displayJobMatch(data) {

    const job = data.job;

    if (jobInfo) {

        jobInfo.innerHTML = `
            <h2>${job.title || "Job"}</h2>
            <p><strong>Company:</strong> ${job.company || "Not specified"}</p>
            <p><strong>Location:</strong> ${job.location || "Not specified"}</p>
            <p><strong>Experience:</strong> ${job.experience_required || "Not specified"}</p>
            <p><strong>Required Skills:</strong> ${job.required_skills || "Not specified"}</p>
        `;

    }


    if (matchScore) {

        matchScore.textContent =
            `${data.match_score || 0}%`;

    }


    // =========================
    // MATCHED SKILLS
    // =========================

    if (matchedSkills) {

        matchedSkills.innerHTML = "";

        if (
            data.matched_skills &&
            data.matched_skills.length > 0
        ) {

            data.matched_skills.forEach(
                function (skill) {

                    const li =
                        document.createElement("li");

                    li.textContent = skill;

                    matchedSkills.appendChild(li);

                }
            );

        } else {

            const li =
                document.createElement("li");

            li.textContent =
                "No matching skills found.";

            matchedSkills.appendChild(li);

        }

    }


    // =========================
    // MISSING SKILLS
    // =========================

    if (missingSkills) {

        missingSkills.innerHTML = "";

        if (
            data.missing_skills &&
            data.missing_skills.length > 0
        ) {

            data.missing_skills.forEach(
                function (skill) {

                    const li =
                        document.createElement("li");

                    li.textContent = skill;

                    missingSkills.appendChild(li);

                }
            );

        } else {

            const li =
                document.createElement("li");

            li.textContent =
                "No missing skills.";

            missingSkills.appendChild(li);

        }

    }

}

// =========================
// BACK TO JOBS
// =========================

const goBackToJobs =
    document.getElementById("goBackToJobs");

if (goBackToJobs) {

    goBackToJobs.onclick = function () {

        window.location.href = "jobs.html";

    };

}


// =========================
// START
// =========================

loadJobMatch();