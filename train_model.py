import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

file_path_csv = './heart_disease_uci.csv'
heart_data = pd.read_csv(file_path_csv)

# Convert target column to binary
heart_data['num'] = (heart_data['num'] > 0).astype(int)

# Drop unnecessary columns
if 'id' in heart_data.columns:
    heart_data = heart_data.drop(columns=['id', 'dataset'])

# Define threshold for missing values (drop columns if >30% missing)
missing_value_threshold = 0.3
for column in heart_data.columns:
    missing_percentage = heart_data[column].isnull().mean()
    if missing_percentage > missing_value_threshold:
        heart_data = heart_data.drop(columns=[column])
    else:
        # Fill missing values
        if heart_data[column].dtype in ['float64', 'int64']:
            heart_data[column] = heart_data[column].fillna(heart_data[column].median())
        else:
            heart_data[column] = heart_data[column].fillna(heart_data[column].mode()[0])
            heart_data[column] = heart_data[column].infer_objects()

# Identify categorical and numerical features
categorical_features = heart_data.select_dtypes(include=['object','bool']).columns.tolist()
numerical_features = heart_data.select_dtypes(include=['float64', 'int64']).columns.drop('num').tolist()

# Encode categorical features
label_encoders = {}
for column in categorical_features:
    le = LabelEncoder()
    heart_data[column] = le.fit_transform(heart_data[column])
    label_encoders[column] = le

# Scale numerical features
scaler = StandardScaler()
heart_data[numerical_features] = scaler.fit_transform(heart_data[numerical_features])

# Define features and target
X = heart_data.drop(columns=['num'])
y_binary = heart_data['num']

# Save feature names for inference
feature_names = X.columns.tolist()
joblib.dump(feature_names, "feature_names.pkl")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)

# Train model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Save model, scaler, and encoders
joblib.dump(rf_model, "heart_failure_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("✅ Model, scaler, and encoders saved successfully!")