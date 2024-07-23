document.getElementById('scraperForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    document.getElementById('loading').style.display = 'block';
    document.getElementById('response').innerHTML = '';

    fetch('/submit', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('response').innerHTML = data;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('response').innerText = 'An error occurred. Please try again.';
        });
});

document.getElementById('approach').addEventListener('change', function (event) {
    const approach = event.target.value;
    document.getElementById('companyNameField').style.display = approach === 'generalized' ? 'block' : 'none';
    document.getElementById('companyURLField').style.display = approach === 'specific' ? 'block' : 'none';
});
