from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import os
import numpy as np

app = Flask(__name__)
CORS(app)

# Load your trained model (only once at the start)
model = joblib.load('model_filename.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request (JSON)
        data = request.get_json()

        # Check if all expected fields are present
        required_fields = ["crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat"]
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Create a DataFrame from the input data
        input_data = [[
            data['crim'], data['zn'], data['indus'], data['chas'], data['nox'],
            data['rm'], data['age'], data['dis'], data['rad'], data['tax'],
            data['ptratio'], data['b'], data['lstat']
        ]]
        df_data = pd.DataFrame(input_data, columns=required_fields)

        # Ensure 'chas' is numeric
        df_data["chas"] = pd.to_numeric(df_data["chas"], errors='coerce')

        # Predict using the pre-loaded model
        prediction = model.predict(df_data)

        # Convert the prediction to a human-readable format (e.g., scaling the result)
        result = float(prediction[0]) * 1000

        # Return the prediction as a JSON response
        return jsonify({'price': result})

    except Exception as e:
        # Return a 500 Internal Server Error with the exception message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

