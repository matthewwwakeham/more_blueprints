document.addEventListener("DOMContentLoaded", () => {
    // Clear the inputs when the page is refreshed
    document.getElementById('username').value = '';
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
    document.getElementById('confirm-password').value = '';

    // Clear any existing error messages
    document.getElementById('usernameError').textContent = '';
    document.getElementById('emailError').textContent = '';
    document.getElementById('passwordError').textContent = '';
    document.getElementById('confirmPasswordError').textContent = '';
    
    // Add event listeners for real-time validation
    document.getElementById('username').addEventListener('input', validateUsername);
    document.getElementById('email').addEventListener('input', validateEmail);
    document.getElementById('password').addEventListener('input', validatePassword);
    document.getElementById('confirm-password').addEventListener('input', validateConfirmPassword);
});

function validateUsername() {
    const username = document.getElementById('username').value;
    const usernamePattern = /^[a-zA-Z0-9]+$/;
    if (username.length < 3 || username.length > 15 || !usernamePattern.test(username)) {
        document.getElementById('usernameError').textContent = 'Username must be 3-15 characters long and contain only letters and numbers.';
        return false;
    } else {
        document.getElementById('usernameError').textContent = '';
        return true;
    }
}

function validateEmail() {
    const email = document.getElementById('email').value;
    if (email.length > 254 || !email.includes('@') || !email.includes('.')) {
        document.getElementById('emailError').textContent = 'Please enter a valid email address with no more than 254 characters.';
        return false;
    } else {
        document.getElementById('emailError').textContent = '';
        return true;
    }
}

function validatePassword() {
    const password = document.getElementById('password').value;
    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_\-+={}[\]:;"'|\\<>,.?/~`]).{8,}$/;
    if (password.length < 8 || !passwordPattern.test(password)) {
        document.getElementById('passwordError').textContent = 'Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, one number, and one special character.';
        return false;
    } else {
        document.getElementById('passwordError').textContent = '';
        return true;
    }
}

function validateConfirmPassword() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    if (confirmPassword !== password) {
        document.getElementById('confirmPasswordError').textContent = 'Passwords do not match. Please confirm your password.';
        return false;
    } else {
        document.getElementById('confirmPasswordError').textContent = '';
        return true;
    }
}

// Final validation function to check all fields before submission
function validateForm() {
    const isUsernameValid = validateUsername();
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    const isConfirmPasswordValid = validateConfirmPassword();

    return isUsernameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid;
}