/**
 * Dayflow Main Logic
 * Handles Authentication (JWT), Sidebar Toggles, and API Interactions.
 */

document.addEventListener("DOMContentLoaded", () => {
    
    // 1. GLOBAL: Highlight Active Sidebar Link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // 2. LOGIN PAGE: Intercept Form Submission
    // We must stop the default form submit to handle the JSON response
    const loginForm = document.querySelector('form[action="/login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // 3. LOGOUT: Handle Logout Click
    const logoutLink = document.querySelector('a[href="/logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});

// ==========================================
// 🔐 AUTHENTICATION LOGIC
// ==========================================

async function handleLogin(event) {
    event.preventDefault(); // Stop page reload

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Map form fields to API expected keys
    // The HTML uses 'login_id' but API might expect 'login_id' or 'email'
    const payload = {
        login_id: data.login_id, 
        password: data.password
    };

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerText;
    submitBtn.innerText = "Signing in...";
    submitBtn.disabled = true;

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            // SUCCESS: Save Token
            localStorage.setItem('access_token', result.token);
            localStorage.setItem('user_role', result.role);
            
            // Redirect to Dashboard
            window.location.href = '/dashboard'; 
        } else {
            // ERROR: Show message
            alert(result.message || 'Login failed');
            submitBtn.innerText = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Login Error:', error);
        alert('An error occurred. Is the backend running?');
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    window.location.href = '/login'; // Or '/' depending on your route
}

// ==========================================
// 🕒 ATTENDANCE LOGIC
// ==========================================

async function triggerCheckIn() {
    const token = localStorage.getItem('access_token');

    if (!token) {
        alert("Session expired. Please log in again.");
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch('/api/attendance/checkin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        const result = await response.json();

        if (response.ok) {
            // Success UX
            alert("✅ Checked In Successfully at " + new Date().toLocaleTimeString());
            window.location.reload(); // Refresh to update status on screen
        } else {
            // Error UX
            alert("⚠️ " + result.message);
        }
    } catch (error) {
        console.error('Check-in Error:', error);
        alert("Failed to connect to server.");
    }
}

// ==========================================
// 🛫 LEAVE LOGIC (Generic Form Handler)
// ==========================================
// This finds any form with class 'api-form' and submits it via JSON
// You can add class="api-form" to your Leave form in leave.html

const apiForms = document.querySelectorAll('.api-form');
apiForms.forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('access_token');
        const action = form.getAttribute('action'); // e.g., /api/leave/apply
        
        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            if (response.ok) {
                alert("Success: " + result.message);
                window.location.reload();
            } else {
                alert("Error: " + result.message);
            }
        } catch (error) {
            console.error(error);
        }
    });
});