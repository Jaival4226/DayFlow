// 1. LOGIN LOGIC
async function handleLogin(event) {
    event.preventDefault();
    const form = event.target;
    const payload = Object.fromEntries(new FormData(form).entries());

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            // Save token for API calls
            localStorage.setItem('access_token', result.token);
            // Redirect to dashboard
            window.location.href = '/dashboard';
        } else {
            alert(result.message || 'Login failed');
        }
    } catch (error) {
        console.error('Login Error:', error);
        alert('Could not connect to the server.');
    }
}

// 2. CHECK-IN / CHECK-OUT LOGIC
async function triggerCheckIn() {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('/api/attendance/clock-in', {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("✅ Checked In Successfully!");
            location.reload(); // Reload to update the card status
        } else {
            // NEW (Correct)
            alert("⚠️ " + (data.message || data.error));
        }
    } catch (error) {
        console.error(error);
        alert("Failed to connect.");
    }
}

async function triggerCheckOut() {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('/api/attendance/clock-out', {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("👋 Checked Out. See you tomorrow!");
            location.reload();
        } else {
            // NEW (Correct)
            alert("⚠️ " + (data.message || data.error));
        }
    } catch (error) {
        console.error(error);
    }
}

// Attach listener if on login page
const loginForm = document.getElementById('loginForm');
if(loginForm) {
    loginForm.addEventListener('submit', handleLogin);
}

// ... existing code ...

async function handleLogout() {
    try {
        // 1. Call backend to clear the Flask Session (cookies)
        await fetch('/auth/logout');

        // 2. Clear the JWT Token from LocalStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_role');

        // 3. Redirect to Login Page
        window.location.href = '/login';
    } catch (error) {
        console.error("Logout error:", error);
        // Force redirect even if backend fails
        window.location.href = '/login';
    }
}

// ... (Add this below your handleLogin function)

async function handleSignup(event) {
    event.preventDefault();
    const form = event.target;
    // Convert form data to JSON
    const payload = Object.fromEntries(new FormData(form).entries());

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            alert(`✅ Account Created! Your Login ID is: ${result.login_id}`);
            window.location.href = '/login';
        } else {
            alert("⚠️ " + (result.message || "Registration failed"));
        }
    } catch (error) {
        console.error(error);
        alert("Failed to connect to server.");
    }
}