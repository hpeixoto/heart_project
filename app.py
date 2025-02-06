import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load trained model, scaler, label encoders, and feature names
model = joblib.load("heart_failure_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")
feature_names = joblib.load("feature_names.pkl")

def preprocess_input(data):

    boolean_mappings = {
        "sex": {"Male": 1, "Female": 0},
        "cp": {"typical angina": 1, "atypical angina": 2, "non-anginal": 3, "asymptomatic": 4},
        "fbs": {"True": 1, "False": 0},
        "restecg": {"normal": 0, "lv hypertrophy": 1},
        "exang": {"True": 1, "False": 0}
    }

    for key, value in data.items():
        print(key, value)
        # Convert boolean-like values first
        if key in boolean_mappings:
            if value in boolean_mappings[key]:
                data[key] = boolean_mappings[key][value]
            else:
                return jsonify({"error": f"Invalid boolean value for {key}: {value}"}), 400

    return data


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Convert input data
        data = request.form.to_dict()
        print("Input data", data)

        # Convert numeric values where applicable
        for k in data.keys():
            if k not in label_encoders:
                print(k)
                try:
                    data[k] = float(data[k])
                except ValueError:
                    return jsonify({"error": f"Invalid value for {k}: {data[k]}"}), 400

        # Encode categorical values and process boolean values
        processed_data = preprocess_input(data)
        print("Processed data", processed_data)

        # If an error JSON was returned from preprocess_input, forward it
        if isinstance(processed_data, tuple):  # This means an error message was returned
            return processed_data

        # Convert to DataFrame with correct column order
        df = pd.DataFrame([processed_data], columns=feature_names)

        # Scale numerical features used in the model ['age', 'trestbps', 'chol', 'thalch', 'oldpeak']
        numerical_features = ['age', 'trestbps', 'chol', 'thalch', 'oldpeak']

        print("numerical_features", numerical_features)
        
        df[numerical_features] = scaler.transform(df[numerical_features])

        print("df", df)

        # Predict
        prediction = model.predict(df)
        result = "At Risk" if prediction[0] == 1 else "Not at Risk"

        return jsonify({"prediction": result})

    except Exception as e:
        print("ERRO 500!!!")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
