const loginForm = document.getElementById("loginForm");
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
const guestLogin = document.getElementById("guestLogin");
const loginMessage = document.getElementById("loginMessage");
const forgotPassword = document.getElementById("forgotPassword");
const createAccount = document.getElementById("createAccount");


/* =========================================
   SHOW / HIDE PASSWORD
========================================= */

togglePassword.addEventListener("click", function () {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        togglePassword.textContent = "🙈";

        togglePassword.setAttribute(
            "aria-label",
            "Hide password"
        );

    } else {

        passwordInput.type = "password";

        togglePassword.textContent = "👁";

        togglePassword.setAttribute(
            "aria-label",
            "Show password"
        );
    }

});


/* =========================================
   LOGIN
========================================= */

loginForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const email =
        document.getElementById("email").value.trim();

    const password =
        passwordInput.value.trim();

    loginMessage.textContent = "";

    if (!email || !password) {

        loginMessage.textContent =
            "Please enter your email and password.";

        return;
    }


    /*
        TEMPORARY LOGIN

        Later this will connect to our Flask backend
        and database.
    */

    loginMessage.style.color = "#347f38";

    loginMessage.textContent =
        "Login successful! Opening AgriMind AI...";


    localStorage.setItem(
        "agrimind_user",
        email
    );


    setTimeout(function () {

        window.location.href = "dashboard.html";

    }, 900);

});


/* =========================================
   GUEST LOGIN
========================================= */

guestLogin.addEventListener("click", function () {

    localStorage.setItem(
        "agrimind_guest",
        "true"
    );

    loginMessage.style.color = "#347f38";

    loginMessage.textContent =
        "Welcome to AgriMind AI!";


    setTimeout(function () {

        window.location.href = "dashboard.html";

    }, 700);

});


/* =========================================
   FORGOT PASSWORD
========================================= */

forgotPassword.addEventListener("click", function (event) {

    event.preventDefault();

    alert(
        "Password recovery will be connected to the backend shortly."
    );

});


/* =========================================
   CREATE ACCOUNT
========================================= */

createAccount.addEventListener("click", function (event) {

    event.preventDefault();

    alert(
        "Account registration will be added in the next stage."
    );

});