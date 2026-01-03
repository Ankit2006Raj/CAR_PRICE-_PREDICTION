"""
Car Price Prediction Model Training Script
Retrains the model with current scikit-learn version
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os

print("="*60)
print("CAR PRICE PREDICTION - MODEL TRAINING")
print("="*60)

# Load dataset
print("\n1. Loading dataset...")
try:
    df = pd.read_csv('datasets/train.csv')
    print(f"   ✓ Loaded {len(df)} records")
except:
    # Try alternative dataset
    df = pd.read_csv('datasets/used_cars.csv')
    print(f"   ✓ Loaded {len(df)} records from used_cars.csv")

print(f"   Columns: {list(df.columns)}")

# Data preprocessing
print("\n2. Preprocessing data...")

# Select relevant features based on app.py requirements
feature_mapping = {
    'registered_year': ['Prod. year', 'Year', 'year', 'registered_year'],
    'engine_capacity': ['Engine volume', 'Engine', 'engine', 'engine_capacity'],
    'transmission_type': ['Gear box type', 'Transmission', 'transmission', 'transmission_type'],
    'kms_driven': ['Mileage', 'Kilometers_Driven', 'kms_driven', 'Kms_Driven'],
    'owner_type': ['Owner', 'owner_type', 'Owner_Type'],
    'fuel_type': ['Fuel type', 'Fuel', 'fuel_type', 'Fuel_Type'],
    'max_power': ['Power', 'max_power', 'Max_Power'],
    'seats': ['Seats', 'seats'],
    'mileage': ['mileage', 'Mileage_kmpl'],
    'body_type': ['Category', 'Body_Type', 'body_type']
}

# Map columns
df_processed = pd.DataFrame()
for target_col, possible_names in feature_mapping.items():
    for name in possible_names:
        if name in df.columns:
            df_processed[target_col] = df[name]
            break

# Add target variable
if 'Price' in df.columns:
    df_processed['price'] = df['Price']
elif 'price' in df.columns:
    df_processed['price'] = df['price']

print(f"   ✓ Mapped columns: {list(df_processed.columns)}")

# Clean data
print("\n3. Cleaning data...")
# Remove rows with missing values
df_processed = df_processed.dropna()

# Clean numeric columns
numeric_cols = ['registered_year', 'engine_capacity', 'kms_driven', 'max_power', 'seats', 'mileage', 'price']
for col in numeric_cols:
    if col in df_processed.columns:
        # Remove non-numeric characters
        if df_processed[col].dtype == 'object':
            df_processed[col] = df_processed[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
        # Remove outliers
        df_processed = df_processed[df_processed[col] > 0]

df_processed = df_processed.dropna()
print(f"   ✓ Clean dataset: {len(df_processed)} records")

# Encode categorical variables
print("\n4. Encoding categorical variables...")
label_encoders = {}
categorical_cols = ['transmission_type', 'owner_type', 'fuel_type', 'body_type']

for col in categorical_cols:
    if col in df_processed.columns:
        le = LabelEncoder()
        df_processed[col] = le.fit_transform(df_processed[col].astype(str))
        label_encoders[col] = le
        print(f"   ✓ Encoded {col}: {len(le.classes_)} categories")

# Prepare features and target - use only available columns
available_features = ['registered_year', 'engine_capacity', 'transmission_type', 'kms_driven', 
                      'owner_type', 'fuel_type', 'max_power', 'seats', 'mileage', 'body_type']

# Filter to only use columns that exist
features = [f for f in available_features if f in df_processed.columns]
print(f"\n   Available features: {features}")

# Add missing features with default values
for feat in available_features:
    if feat not in df_processed.columns:
        if feat == 'owner_type':
            df_processed[feat] = 0  # First owner
        elif feat == 'max_power':
            df_processed[feat] = df_processed['engine_capacity'] * 30  # Estimate
        elif feat == 'seats':
            df_processed[feat] = 5  # Default 5 seats
        elif feat == 'mileage':
            df_processed[feat] = 15.0  # Default mileage
        print(f"   ⚠ Added missing feature '{feat}' with default values")

features = available_features
X = df_processed[features]
y = df_processed['price']

print(f"\n5. Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   ✓ Training set: {len(X_train)} samples")
print(f"   ✓ Test set: {len(X_test)} samples")

# Scale features
print("\n6. Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("   ✓ Features scaled")

# Train model
print("\n7. Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_scaled, y_train)
print("   ✓ Model trained")

# Evaluate
print("\n8. Evaluating model...")
y_pred = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"   Mean Absolute Error: ₹{mae:,.2f}")
print(f"   R² Score: {r2:.4f}")

# Save models
print("\n9. Saving models...")
os.makedirs('models', exist_ok=True)

joblib.dump(model, 'models/car_price_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(label_encoders, 'models/label_encoders.pkl')
joblib.dump(features, 'models/features.pkl')

print("   ✓ Saved car_price_model.pkl")
print("   ✓ Saved scaler.pkl")
print("   ✓ Saved label_encoders.pkl")
print("   ✓ Saved features.pkl")

print("\n" + "="*60)
print("MODEL TRAINING COMPLETE!")
print("="*60)
print("\nYou can now run: python app.py")
