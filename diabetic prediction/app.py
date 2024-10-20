from flask import Flask, request, jsonify # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn import svm # type: ignore
from sklearn.metrics import accuracy_score # type: ignore
from flask_cors import CORS  # type: ignore # To handle CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the diabetes dataset and train the model
diabetes_dataset = pd.read_csv('diabetes.csv')
X = diabetes_dataset.drop(columns='Outcome', axis=1)
Y = diabetes_dataset['Outcome']

scaler = StandardScaler()
scaler.fit(X)
standardized_data = scaler.transform(X)
X = standardized_data

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# Train the SVM model
classifier = svm.SVC(kernel='linear')
classifier.fit(X_train, Y_train)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    app.logger.info(f"Received input data: {input_data}")  # Log the incoming request
    
    # Extract and reshape data
    input_values = [
        input_data['pregnancies'],
        input_data['glucose'],
        input_data['blood_pressure'],
        input_data['skin_thickness'],
        input_data['insulin'],
        input_data['bmi'],
        input_data['dpf'],
        input_data['age']
    ]
    
    input_data_as_numpy_array = np.asarray(input_values).reshape(1, -1)
    std_data = scaler.transform(input_data_as_numpy_array)
    
    # Predict and return results
    prediction = classifier.predict(std_data)
    
    if prediction[0] == 0:
        result = {
            "message": "The person is not diabetic.",
            "precautions": [
                "Maintain a healthy diet rich in vegetables, fruits, and whole grains.",
                "Engage in regular physical activity, at least 30 minutes a day.",
                "Stay hydrated by drinking water rather than sugary drinks.",
                "Avoid processed foods and foods high in sugar."
            ],
            "recommended_foods": [
                "Green leafy vegetables like spinach, kale, and broccoli.",
                "Whole grains like oats and quinoa.",
                "Fruits like berries, apples, and pears.",
                "Healthy fats like avocado, nuts, and olive oil."
            ]
        }
    else:
        result = {
            "message": "The person is diabetic.",
            "precautions": [
                "Follow a balanced, low-sugar diet.",
                "Engage in regular exercise to manage weight and blood sugar levels.",
                "Monitor your blood glucose levels regularly.",
                "Avoid foods with a high glycemic index (GI) like refined sugars."
            ],
            "recommended_foods": [
                "Non-starchy vegetables like cucumber, zucchini, and cauliflower.",
                "Lean proteins like chicken, turkey, and tofu.",
                "Whole grains such as brown rice and barley.",
                "Nuts and seeds for healthy fats."
            ]
        }
    
    app.logger.info(f"Prediction result: {result}")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
