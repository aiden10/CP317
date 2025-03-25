
// Make the login form call loginUser when submit is pressed
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const email = loginForm.elements["email"].value.trim();
        const password = loginForm.elements["password"].value.trim();
        loginUser(email, password);
    });
});

function loginUser(email, password) {
    /*
    Parameters:
        - email: the email address from the login form
        - password: the password from the login form
    Sends a POST request containing email and password to server. Redirects to dashboard and stores session token in cookies on successful request. 
    */
    const messageLabel = document.getElementById("message-label");

    fetch("http://localhost:8000/login", { // [CHANGE] update this to the port the server will be hosted on, or the actual address if we host the backend online
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200) {
            messageLabel.style.display = "block"
            messageLabel.innerText = data.message;
            messageLabel.style.color = "green";

            document.cookie = "session_token=" + data.session_token + "; path=/; Secure";

            setTimeout(() => {
                window.location.href = "../dashboard/dashboard.html";
            }, 1000);
        } else {
            messageLabel.style.display = "block"
            messageLabel.innerText = data.message;
            messageLabel.style.color = "red";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        messageLabel.style.display = "block"
        messageLabel.innerText = error;
        messageLabel.style.color = "red";
    });
}