document.getElementById('diabetesForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const data = {
        pregnancies: parseFloat(document.getElementById('pregnancies').value),
        glucose: parseFloat(document.getElementById('glucose').value),
        blood_pressure: parseFloat(document.getElementById('bloodPressure').value),
        skin_thickness: parseFloat(document.getElementById('skinThickness').value),
        insulin: parseFloat(document.getElementById('insulin').value),
        bmi: parseFloat(document.getElementById('bmi').value),
        dpf: parseFloat(document.getElementById('dpf').value),
        age: parseFloat(document.getElementById('age').value)
    };

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        let resultHTML = `
            <div class="card">
                <div class="card-header">Prediction Result</div>
                <div class="card-body">
                    <h5>${data.message}</h5>
                    <h6>Precautions:</h6>
                    <ul class="precautions">`;

        data.precautions.forEach(function(item) {
            resultHTML += `<li>${item}</li>`;
        });

        resultHTML += `</ul>
                    <h6>Recommended Foods:</h6>
                    <ul class="recommended-foods">`;

        data.recommended_foods.forEach(function(item) {
            resultHTML += `<li>${item}</li>`;
        });

        resultHTML += `</ul>
                </div>
            </div>`;

        document.getElementById('result').innerHTML = resultHTML;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
