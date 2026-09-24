const uploadForm =
    document.getElementById("uploadForm");


uploadForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const fileInput =
            document.getElementById("resumeFile");

        const message =
            document.getElementById("uploadMessage");

        const file =
            fileInput.files[0];


        // =========================
        // CHECK FILE
        // =========================

        if (!file) {

            message.textContent =
                "Please select your resume.";

            return;
        }


        // =========================
        // CHECK FILE TYPE
        // =========================

        const fileName =
            file.name.toLowerCase();

        const allowed =
            fileName.endsWith(".pdf") ||
            fileName.endsWith(".docx");


        if (!allowed) {

            message.textContent =
                "Please upload a PDF or DOCX file.";

            return;
        }


        // =========================
        // CHECK FILE SIZE
        // =========================

        if (file.size > 10 * 1024 * 1024) {

            message.textContent =
                "File size must be less than 10 MB.";

            return;
        }


        // =========================
        // CHECK LOGIN
        // =========================

        const userData =
            localStorage.getItem("user");


        if (!userData) {

            message.textContent =
                "Please login before uploading.";

            window.location.href =
                "login.html";

            return;
        }


        let user;

        try {

            user =
                JSON.parse(userData);

        } catch (error) {

            localStorage.removeItem("user");

            window.location.href =
                "login.html";

            return;
        }


        if (!user.id) {

            message.textContent =
                "Invalid login session.";

            return;
        }


        // =========================
        // FORM DATA
        // =========================

        const formData =
            new FormData();

        formData.append(
            "resume",
            file
        );

        formData.append(
            "user_id",
            user.id
        );


        message.textContent =
            "Uploading resume...";


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/api/upload-resume",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            console.log(
                "Upload Response:",
                data
            );


            if (!response.ok) {

                message.textContent =
                    data.message ||
                    "Resume upload failed.";

                return;
            }


            if (
                data.status !== "success" ||
                !data.resume_id
            ) {

                message.textContent =
                    "Resume upload response is invalid.";

                return;
            }


            // =========================
            // SAVE RESUME ID
            // =========================

            localStorage.setItem(
                "resume_id",
                data.resume_id
            );


            message.textContent =
                "Resume uploaded successfully!";


            // =========================
            // GO TO RESULT
            // =========================

            setTimeout(
                function () {

                    window.location.href =
                        "result.html";

                },
                500
            );


        } catch (error) {

            console.error(
                "Upload Error:",
                error
            );

            message.textContent =
                "Unable to connect to the backend.";

        }

    }
);