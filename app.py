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
    # Get the data from the request (JSON)
    data = request.json

    # Define the expected columns
    columns = ["crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat"]

    # Create a DataFrame from the input data
    input_data = [[
        data['crim'], data['zn'], data['indus'], data['chas'], data['nox'],
        data['rm'], data['age'], data['dis'], data['rad'], data['tax'],
        data['ptratio'], data['b'], data['lstat']
    ]]
    df_data = pd.DataFrame(input_data, columns=columns)

    # Ensure 'chas' is numeric
    df_data["chas"] = pd.to_numeric(df_data["chas"], errors='coerce')

    # Predict using the pre-loaded model
    result = model.predict(df_data)

    # Convert the prediction to a human-readable format (e.g., scaling the result)
    prediction = float(result[0]) * 1000

    # Return the prediction as a JSON response
    return jsonify({'price': prediction})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

