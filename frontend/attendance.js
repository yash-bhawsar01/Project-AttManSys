// Toggle method
document.getElementById('method').addEventListener('change', function () {
    const method = this.value;
    document.getElementById('manualForm').style.display = method === 'manual' ? 'block' : 'none';
    document.getElementById('facialForm').style.display = method === 'facial' ? 'block' : 'none';
  });
  
  // Manual attendance
  document.getElementById('attendanceForm').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const studentId = document.getElementById('studentId').value;
    const status = document.getElementById('status').value;
    const message = document.getElementById('attendanceMessage');
  
    message.style.color = 'green';
    message.textContent = `Attendance for ${studentId} marked as ${status}.`;
  
    // Later: Send to backend
  });
  
  // Facial upload
  document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const studentId = document.getElementById('faceStudentId').value;
    const faceImage = document.getElementById('faceImage').files[0];
    const message = document.getElementById('facialMessage');
  
    if (!faceImage) {
      message.style.color = 'red';
      message.textContent = 'Please select an image!';
      return;
    }
  
    message.style.color = 'green';
    message.textContent = `Face data for ${studentId} uploaded (simulated).`;
  
    // Later: Send image to backend for processing
  });
  