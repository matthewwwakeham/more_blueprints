document.addEventListener("DOMContentLoaded", () => {
    // Clear the inputs when the page is refreshed
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
});

// Validate login form
function validateForm() {
    let valid = true;

    // Username Validation
    const username = document.getElementById('username').value;
    const usernamePattern = /^[a-zA-Z0-9]+$/; // Only allow alphanumeric characters
    if (username.length < 3 || username.length > 15 || !usernamePattern.test(username)) {
        // Do not show an error message here
        valid = false;
    }

    // Password Validation
    const password = document.getElementById('password').value;
    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_\-+={}[\]:;"'|\\<>,.?/~`]).{8,}$/;
    if (password.length < 8 || !passwordPattern.test(password)) {
        // Do not show an error message here
        valid = false;
    }

    return valid; // Only submit if all fields are valid
}