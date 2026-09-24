const jobsList = document.getElementById("jobsList");


// =========================
// LOAD JOBS
// =========================

async function loadJobs() {

    if (!jobsList) {
        return;
    }

    jobsList.innerHTML =
        "<p>Loading jobs...</p>";

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/jobs"
        );

        const data = await response.json();

        console.log("Jobs Response:", data);

        if (
            !response.ok ||
            data.status !== "success"
        ) {

            throw new Error(
                data.message || "Unable to load jobs."
            );

        }

        jobsList.innerHTML = "";

        if (
            !data.jobs ||
            data.jobs.length === 0
        ) {

            jobsList.innerHTML =
                "<p>No jobs available.</p>";

            return;

        }

        data.jobs.forEach(function (job) {

            const card =
                document.createElement("div");

            card.className = "job-card";

            const title =
                document.createElement("h3");

            title.textContent =
                job.title || "Job";

            const company =
                document.createElement("p");

            company.textContent =
                `Company: ${job.company || "Not specified"}`;

            const location =
                document.createElement("p");

            location.textContent =
                `Location: ${job.location || "Not specified"}`;

            const experience =
                document.createElement("p");

            experience.textContent =
                `Experience: ${job.experience_required || "Not specified"}`;

            const skills =
                document.createElement("p");

            skills.textContent =
                `Required Skills: ${job.required_skills || "Not specified"}`;

            const button =
                document.createElement("button");

            button.textContent =
                "Find Match";

            button.addEventListener(
                "click",
                function () {

                    const resumeId =
                        localStorage.getItem("resume_id");

                    if (!resumeId) {

                        alert(
                            "Please upload a resume first."
                        );

                        window.location.href =
                            "upload.html";

                        return;

                    }

                    localStorage.setItem(
                        "selected_job_id",
                        job.id
                    );

                    window.location.href =
                        "job-match.html";

                }
            );

            card.appendChild(title);
            card.appendChild(company);
            card.appendChild(location);
            card.appendChild(experience);
            card.appendChild(skills);
            card.appendChild(button);

            jobsList.appendChild(card);

        });

    } catch (error) {

        console.error(
            "Jobs Error:",
            error
        );

        jobsList.innerHTML =
            "<p>Unable to load jobs.</p>";

    }

}


// =========================
// START
// =========================

loadJobs();