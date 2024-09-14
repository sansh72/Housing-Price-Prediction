document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();

        // Collect form data
        const formData = {
            crim: parseFloat(document.getElementById('crim').value),
            zn: parseFloat(document.getElementById('zn').value),
            indus: parseFloat(document.getElementById('indus').value),
            chas: parseFloat(document.getElementById('chas').value),
            nox: parseFloat(document.getElementById('nox').value),
            rm: parseFloat(document.getElementById('rm').value),
            age: parseFloat(document.getElementById('age').value),
            dis: parseFloat(document.getElementById('dis').value),
            rad: parseFloat(document.getElementById('rad').value),
            tax: parseFloat(document.getElementById('tax').value),
            ptratio: parseFloat(document.getElementById('ptratio').value),
            b: parseFloat(document.getElementById('b').value),
            lstat: parseFloat(document.getElementById('lstat').value)
        };

        // Send data to Flask API via POST request
        fetch('https://housing-price-prediction-1.onrender.com//predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display the predicted price in the output div
            document.getElementById('output').innerText = `Predicted House Price: $${data.price.toFixed(2)}`;
        })
        .catch(error => {
            // Handle errors and show in the output div
            document.getElementById('output').innerText = `Error: ${error.message}`;
            console.error('Error:', error);
        });
    });
