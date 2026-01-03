from flask import Flask, render_template, request, jsonify, session
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'car_price_predictor_secret_key_2024'

# Load model and encoders
print('Loading models...')
model = joblib.load('models/car_price_model.pkl')
scaler = joblib.load('models/scaler.pkl')
label_encoders = joblib.load('models/label_encoders.pkl')
features = joblib.load('models/features.pkl')
print('✓ Models loaded successfully')

# History file
HISTORY_FILE = 'data/prediction_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_prediction(data):
    history = load_history()
    history.append(data)
    if len(history) > 100:  # Keep last 100 predictions
        history = history[-100:]
    os.makedirs('data', exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def get_market_insights(year, kms, price):
    """Generate market insights based on prediction"""
    car_age = 2024 - int(year)
    avg_kms_per_year = float(kms) / car_age if car_age > 0 else float(kms)
    
    insights = []
    
    # Mileage insight
    if avg_kms_per_year < 10000:
        insights.append({'type': 'success', 'text': 'Low mileage - Great value!'})
    elif avg_kms_per_year > 20000:
        insights.append({'type': 'warning', 'text': 'High mileage - Price may be affected'})
    
    # Age insight
    if car_age <= 3:
        insights.append({'type': 'success', 'text': 'Nearly new - Good resale value'})
    elif car_age >= 10:
        insights.append({'type': 'info', 'text': 'Older vehicle - Consider maintenance costs'})
    
    # Price range
    if price < 300000:
        insights.append({'type': 'info', 'text': 'Budget-friendly option'})
    elif price > 1000000:
        insights.append({'type': 'success', 'text': 'Premium segment vehicle'})
    
    return insights

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def get_history():
    """Get prediction history"""
    try:
        history = load_history()
        return jsonify({'success': True, 'history': history[-10:]})  # Last 10
    except:
        return jsonify({'success': True, 'history': []})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Validate input
        required_fields = ['year', 'engine', 'transmission', 'kms', 'owner', 'fuel', 'power', 'seats', 'mileage', 'body']
        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create input array
        input_data = {
            'registered_year': int(data['year']),
            'engine_capacity': float(data['engine']),
            'transmission_type': data['transmission'],
            'kms_driven': float(data['kms']),
            'owner_type': data['owner'],
            'fuel_type': data['fuel'],
            'max_power': float(data['power']),
            'seats': int(data['seats']),
            'mileage': float(data['mileage']),
            'body_type': data['body']
        }
        
        # Encode categorical variables
        for col in ['transmission_type', 'owner_type', 'fuel_type', 'body_type']:
            try:
                input_data[col] = label_encoders[col].transform([input_data[col]])[0]
            except:
                input_data[col] = 0
        
        # Create DataFrame
        input_df = pd.DataFrame([input_data], columns=features)
        
        # Scale and predict
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        
        # Format price
        if prediction >= 10000000:
            price_str = f"₹ {prediction/10000000:.2f} Crore"
        else:
            price_str = f"₹ {prediction/100000:.2f} Lakh"
        
        # Get market insights
        insights = get_market_insights(data['year'], data['kms'], prediction)
        
        # Calculate depreciation
        car_age = 2024 - int(data['year'])
        depreciation_rate = (car_age * 10) if car_age <= 5 else 50
        
        # Save to history
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'year': data['year'],
            'kms': data['kms'],
            'fuel': data['fuel'],
            'transmission': data['transmission'],
            'price': float(prediction),
            'price_formatted': price_str
        }
        save_prediction(history_entry)
        
        return jsonify({
            'success': True,
            'price': price_str,
            'price_value': float(prediction),
            'insights': insights,
            'depreciation': depreciation_rate,
            'car_age': car_age
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid input values'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/compare', methods=['POST'])
def compare():
    """Compare multiple predictions"""
    try:
        predictions = request.json.get('predictions', [])
        if len(predictions) < 2:
            return jsonify({'success': False, 'error': 'Need at least 2 cars to compare'})
        
        comparison = {
            'best_value': min(predictions, key=lambda x: x['price_value']),
            'highest_price': max(predictions, key=lambda x: x['price_value']),
            'average_price': sum(p['price_value'] for p in predictions) / len(predictions)
        }
        
        return jsonify({'success': True, 'comparison': comparison})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print('\n' + '='*60)
    print('CAR PRICE PREDICTION API - PRODUCTION READY')
    print('='*60)
    print('\nServer starting on http://localhost:5000')
    print('Press CTRL+C to quit\n')
    app.run(debug=True, host='0.0.0.0', port=5000)
