function signup() {
    const roleSelected = document.querySelector('input[name="role"]:checked');
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('passwordSignup').value.trim();
    const mobile = document.getElementById('mobile').value.trim();
    const agreed = document.getElementById('terms').checked;

    if (!roleSelected) {
        alert('Please select a role (Buyer, Agent, Builder).');
        return;
    }

    if (!name || !email || !password || !mobile) {
        alert('Please fill in all fields.');
        return;
    }

    if (!validateEmail(email)) {
        alert('Invalid email address.');
        return;
    }

    if (password.length < 6) {
        alert('Password should be at least 6 characters.');
        return;
    }

    if (!/^\d{10}$/.test(mobile)) {
        alert('Mobile number must be exactly 10 digits.');
        return;
    }

    if (!agreed) {
        alert('Please agree to the Terms & Conditions.');
        return;
    }

    alert('Sign-up successful! Redirecting to login page...');
    window.location.href = 'index.html';
}

function validateEmail(email) {
    // Basic email regex pattern
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
}

// Optional: Enter key triggers signup
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        signup();
    }
});
