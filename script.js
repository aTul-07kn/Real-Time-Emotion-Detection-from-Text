function submitForm() {
    var form = document.getElementById("feedbackForm");
    var formData = new FormData(form);

    // Send the form data to the backend using fetch or another method
    // Example using fetch:
    fetch('your_backend_url', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the backend as needed
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
