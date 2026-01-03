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
            // SUCCESS: Store the session data
            localStorage.setItem('access_token', result.token);
            localStorage.setItem('user_role', result.role);
            
            // REDIRECT: This is what actually shows the next page
            window.location.href = '/dashboard'; 
        } else {
            alert(result.message || 'Login failed');
        }
    } catch (error) {
        console.error('Login Error:', error);
        alert('Could not connect to the server.');
    }
}