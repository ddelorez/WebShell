// static/login.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(new FormData(this))
        }).then(response => {
            if (response.ok) {
                window.location.href = "/terminal";
            } else {
                return response.json();
            }
        }).then(data => {
            if (data && data.status === "error") {
                document.getElementById('errorMessage').textContent = data.message;
            }
        });
    });
});