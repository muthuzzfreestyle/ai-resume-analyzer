const registerForm =
    document.getElementById("registerForm");

const loginForm =
    document.getElementById("loginForm");


// =========================
// REGISTER
// =========================

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const name =
                document.getElementById("name").value.trim();

            const email =
                document.getElementById("email").value.trim();

            const password =
                document.getElementById("password").value;

            const message =
                document.getElementById("registerMessage");


            message.textContent =
                "Creating account...";


            try {

                const response =
                    await fetch(
                        "http://127.0.0.1:5000/api/register",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                name: name,
                                email: email,
                                password: password
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    message.textContent =
                        data.message ||
                        "Registration failed.";

                    return;
                }


                message.textContent =
                    "Registration successful! Redirecting...";


                setTimeout(
                    function () {

                        window.location.href =
                            "login.html";

                    },
                    1000
                );


            } catch (error) {

                console.error(
                    "Registration Error:",
                    error
                );

                message.textContent =
                    "Unable to connect to the backend.";

            }

        }
    );

}


// =========================
// LOGIN
// =========================

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const email =
                document.getElementById("email").value.trim();

            const password =
                document.getElementById("password").value;

            const message =
                document.getElementById("loginMessage");


            message.textContent =
                "Logging in...";


            try {

                const response =
                    await fetch(
                        "http://127.0.0.1:5000/api/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                email: email,
                                password: password
                            })
                        }
                    );


                const data =
                    await response.json();


                console.log(
                    "Login Response:",
                    data
                );


                if (!response.ok) {

                    message.textContent =
                        data.message ||
                        "Login failed.";

                    return;
                }


                if (
                    data.status !== "success" ||
                    !data.user
                ) {

                    message.textContent =
                        "Login response is invalid.";

                    return;
                }


                // =========================
                // SAVE USER SESSION
                // =========================

                localStorage.setItem(
                    "user",
                    JSON.stringify(data.user)
                );


                message.textContent =
                    "Login successful! Redirecting...";


                // =========================
                // GO TO DASHBOARD
                // =========================

                setTimeout(
                    function () {

                        window.location.href =
                            "dashboard.html";

                    },
                    500
                );

            } catch (error) {

                console.error(
                    "Login Error:",
                    error
                );

                message.textContent =
                    "Unable to connect to the backend.";

            }

        }
    );

}