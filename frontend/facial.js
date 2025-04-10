document.getElementById('facialForm').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const studentId = document.getElementById('studentId').value;
    const faceImage = document.getElementById('faceImage').files[0];
    const message = document.getElementById('facialMessage');
  
    if (!faceImage) {
      message.style.color = 'red';
      message.textContent = 'Please select an image!';
      return;
    }
  
    // Show dummy response for now
    message.style.color = 'green';
    message.textContent = `Face data for ${studentId} uploaded (simulated).`;
  
    // Later: send to backend using FormData + fetch
  });
  