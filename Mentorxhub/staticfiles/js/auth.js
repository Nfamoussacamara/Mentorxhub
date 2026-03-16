// MentorXHub - Auth Logic

document.addEventListener('DOMContentLoaded', () => {
    // Standard Django form submission is used now.
    // This file can be used for client-side validation if needed.

    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            // Optional: Client-side password match check
            // But Django forms handle this too.
            // We allow default submission.
        });
    }
});
