document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const formData = new FormData(event.target);
    const uploadMessage = document.getElementById('upload-message');
    const loader = document.getElementById('loader');

    // Show the loader
    loader.style.display = 'block';

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      uploadMessage.textContent = data;
      setTimeout(() => {
        uploadMessage.textContent = '';
      }, 3000); // Clear the message after 3 seconds
    })
    .catch(error => {
      uploadMessage.textContent = 'Error uploading image';
      console.error('Error:', error);
    })
    .finally(() => {
      // Hide the loader
      loader.style.display = 'none';
    });
  });