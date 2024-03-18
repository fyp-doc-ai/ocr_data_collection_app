document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const formData = new FormData(event.target);
    const loader = document.getElementById('loader');

    // Show the loader
    loader.style.display = 'block';

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      appendAlert(data, 'success');
    })
    .catch(error => {
      appendAlert('Error uploading image', 'danger');
      console.error('Error:', error);
    })
    .finally(() => {
      // Hide the loader
      loader.style.display = 'none';
    });
  });

const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  const alertPlaceholder = document.getElementById('upload-message');
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible my-3" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')
  alertPlaceholder.append(wrapper)
}