document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirmPassword').value.trim();
    const role = document.getElementById('role').value;
  
    const message = document.getElementById('registerMessage');
  
    if (password !== confirmPassword) {
      message.style.color = 'red';
      message.textContent = 'Passwords do not match!';
      return;
    }
  
    // Dummy success message for now
    message.style.color = 'green';
    message.textContent = 'Registration successful!';
  
    // Later: Replace with real fetch to backend
    /*
    fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password, role })
    })
      .then(response => response.json())
      .then(data => {
        message.textContent = data.message;
      });
    */
  });
  