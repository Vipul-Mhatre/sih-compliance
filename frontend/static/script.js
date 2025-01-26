document.getElementById('runAuditBtn').addEventListener('click', function() {
    fetch('/api/audit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ os_type: 'windows' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('result').innerText = data.message;
            fetch('/api/results')
                .then(response => response.json())
                .then(results => {
                    document.getElementById('result').innerText = JSON.stringify(results, null, 2);
                });
        } else if (data.error) {
            document.getElementById('result').innerText = data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred while running the audit.';
    });
});