const user = JSON.parse(
    localStorage.getItem("user") || "null"
);

const historyList =
    document.getElementById("historyList");


// =========================
// CHECK LOGIN
// =========================

if (!user) {

    window.location.href = "login.html";

}


// =========================
// LOAD RESUME HISTORY
// =========================

async function loadResumeHistory() {

    if (!historyList || !user) {
        return;
    }

    historyList.innerHTML =
        "<p>Loading resume history...</p>";

    try {

        const response = await fetch(
            `http://127.0.0.1:5000/api/user/${user.id}/resumes`
        );

        const data = await response.json();

        if (
            !response.ok ||
            data.status !== "success"
        ) {

            throw new Error(
                data.message ||
                "Unable to load resume history."
            );

        }

        historyList.innerHTML = "";

        if (
            !data.resumes ||
            data.resumes.length === 0
        ) {

            historyList.innerHTML =
                "<p>No resumes uploaded yet.</p>";

            return;

        }


        data.resumes.forEach(function (resume) {

            const card =
                document.createElement("div");

            card.className = "card";


            const title =
                document.createElement("h3");

            title.textContent =
                resume.file_name;


            const date =
                document.createElement("p");

            date.textContent =
                `Uploaded: ${new Date(
                    resume.uploaded_at
                ).toLocaleString()}`;


            const score =
                document.createElement("p");

            score.textContent =
                `ATS Score: ${
                    resume.ats_score !== null
                        ? resume.ats_score + "%"
                        : "Not analyzed"
                }`;


            const skills =
                document.createElement("p");

            skills.textContent =
                `Skill Score: ${
                    resume.skill_score !== null
                        ? resume.skill_score + "%"
                        : "Not available"
                }`;


            const education =
                document.createElement("p");

            education.textContent =
                `Education Score: ${
                    resume.education_score !== null
                        ? resume.education_score + "%"
                        : "Not available"
                }`;


            const experience =
                document.createElement("p");

            experience.textContent =
                `Experience Score: ${
                    resume.experience_score !== null
                        ? resume.experience_score + "%"
                        : "Not available"
                }`;


            const formatting =
                document.createElement("p");

            formatting.textContent =
                `Formatting Score: ${
                    resume.formatting_score !== null
                        ? resume.formatting_score + "%"
                        : "Not available"
                }`;


            // =========================
            // VIEW ANALYSIS BUTTON
            // =========================

            const viewButton =
                document.createElement("button");

            viewButton.textContent =
                "View Analysis";

            viewButton.addEventListener(
                "click",
                function () {

                    localStorage.setItem(
                        "resume_id",
                        resume.id
                    );

                    window.location.href =
                        "result.html";

                }
            );


            // =========================
            // DOWNLOAD BUTTON
            // =========================

            const downloadButton =
                document.createElement("button");

            downloadButton.textContent =
                "Download Resume";

            downloadButton.addEventListener(
                "click",
                function () {

                    window.open(
                        `http://127.0.0.1:5000/api/resume/${resume.id}/download`,
                        "_blank"
                    );

                }
            );


            // =========================
            // DELETE BUTTON
            // =========================

            const deleteButton =
                document.createElement("button");

            deleteButton.textContent =
                "Delete Resume";

            deleteButton.addEventListener(
                "click",
                async function () {

                    const confirmed =
                        confirm(
                            "Are you sure you want to delete this resume?"
                        );

                    if (!confirmed) {
                        return;
                    }

                    try {

                        const response =
                            await fetch(
                                `http://127.0.0.1:5000/api/resume/${resume.id}`,
                                {
                                    method: "DELETE"
                                }
                            );

                        const data =
                            await response.json();

                        if (
                            !response.ok ||
                            data.status !== "success"
                        ) {

                            throw new Error(
                                data.message ||
                                "Unable to delete resume."
                            );

                        }

                        alert(
                            "Resume deleted successfully."
                        );

                        loadResumeHistory();

                    } catch (error) {

                        console.error(
                            "Delete Error:",
                            error
                        );

                        alert(
                            "Unable to delete resume."
                        );

                    }

                }
            );


            card.appendChild(title);
            card.appendChild(date);
            card.appendChild(score);
            card.appendChild(skills);
            card.appendChild(education);
            card.appendChild(experience);
            card.appendChild(formatting);

            card.appendChild(viewButton);
            card.appendChild(downloadButton);
            card.appendChild(deleteButton);

            historyList.appendChild(card);

        });

    } catch (error) {

        console.error(
            "History Error:",
            error
        );

        historyList.innerHTML =
            "<p>Unable to load resume history.</p>";

    }

}

// =========================
// START
// =========================

loadResumeHistory();