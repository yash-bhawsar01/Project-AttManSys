document.getElementById('loginForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  const response = await fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();

  const messageBox = document.getElementById('message');
  if (data.success) {
    messageBox.style.color = 'green';
    messageBox.textContent = "Login successful!";
    // You can redirect to dashboard here
  } else {
    messageBox.style.color = 'red';
    messageBox.textContent = data.message || "Login failed!";
  }
});
