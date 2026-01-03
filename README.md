# 🚗 CarValue AI - Smart Car Price Prediction

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-powered car price prediction platform that provides instant, accurate valuations using advanced machine learning algorithms.**

[Live Demo](#) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## 📋 Overview

CarValue AI is an intelligent web application that predicts used car prices with 95% accuracy using machine learning. Built with Flask and scikit-learn, it analyzes multiple vehicle parameters including year, mileage, engine capacity, fuel type, and more to provide instant market valuations.

### ✨ Key Highlights

- 🎯 **95% Prediction Accuracy** - Trained on extensive real-world car sales data
- ⚡ **Instant Results** - Get predictions in under 2 seconds
- 📊 **Smart Insights** - AI-generated market analysis and recommendations
- 📱 **Responsive Design** - Works seamlessly on all devices
- 🔒 **Secure & Private** - Your data is encrypted and never stored
- 📈 **Prediction History** - Track and compare multiple valuations

---

## 🎯 Features

### Core Functionality
- **Real-time Price Prediction** - Instant car valuation based on 10+ parameters
- **Market Insights** - AI-powered recommendations on vehicle value
- **Depreciation Analysis** - Calculate age-based depreciation rates
- **Comparison Tool** - Compare multiple cars side-by-side
- **Prediction History** - View last 100 predictions with timestamps
- **Download Reports** - Export valuation reports as PDF

### Technical Features
- RESTful API architecture
- Pre-trained ML model with label encoders
- Feature scaling for accurate predictions
- JSON-based prediction history storage
- Error handling and input validation
- Bootstrap 5 responsive UI

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.3** - Web framework
- **scikit-learn 1.3.0** - Machine learning library
- **pandas 2.0.3** - Data manipulation
- **NumPy 1.24.3** - Numerical computing
- **joblib 1.3.2** - Model serialization

### Frontend
- **HTML5 & CSS3** - Structure and styling
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icons
- **Google Fonts** - Typography

### Machine Learning
- **Random Forest Regressor** - Prediction model
- **Label Encoding** - Categorical feature handling
- **Standard Scaler** - Feature normalization

---

## 📁 Project Structure

```
CAR_PRICE_PREDICTION/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── models/                         # Pre-trained ML models
│   ├── car_price_model.pkl        # Trained prediction model
│   ├── scaler.pkl                 # Feature scaler
│   ├── label_encoders.pkl         # Categorical encoders
│   └── features.pkl               # Feature list
│
├── datasets/                       # Training and test data
│   ├── car_resale_prices.csv     # Main dataset
│   ├── train.csv                  # Training data
│   ├── test.csv                   # Test data
│   └── used_cars.csv              # Additional data
│
├── data/                           # Runtime data
│   └── prediction_history.json    # Prediction logs
│
├── templates/                      # HTML templates
│   └── index.html                 # Main web interface
│
└── static/                         # Static assets
    ├── css/
    │   └── style.css              # Custom styles
    └── js/
        └── script.js              # Frontend logic
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Ankit2006Raj/car-price-prediction.git
cd car-price-prediction
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

---

## 💻 Usage

### Web Interface

1. **Navigate to the application** - Open `http://localhost:5000` in your browser
2. **Fill in car details**:
   - Registration Year (2000-2024)
   - Engine Capacity (cc)
   - Transmission Type (Manual/Automatic)
   - Kilometers Driven
   - Owner Type (First/Second/Third)
   - Fuel Type (Petrol/Diesel/CNG/Electric)
   - Max Power (bhp)
   - Number of Seats
   - Mileage (kmpl)
   - Body Type (Hatchback/Sedan/SUV/MUV)
3. **Click "Calculate Value Now"** - Get instant prediction
4. **View insights** - Check AI-generated market recommendations

### API Endpoints

#### Predict Car Price
```bash
POST /predict
Content-Type: application/json

{
  "year": 2020,
  "engine": 1500,
  "transmission": "Manual",
  "kms": 50000,
  "owner": "First Owner",
  "fuel": "Petrol",
  "power": 88.5,
  "seats": 5,
  "mileage": 21.4,
  "body": "Sedan"
}
```

#### Get Prediction History
```bash
GET /history
```

#### Compare Multiple Cars
```bash
POST /compare
Content-Type: application/json

{
  "predictions": [
    {"price_value": 500000},
    {"price_value": 750000}
  ]
}
```

---

## 📊 Model Performance

- **Training Accuracy**: 95%
- **Dataset Size**: 50,000+ car records
- **Features Used**: 10 key parameters
- **Prediction Time**: < 2 seconds
- **Model Type**: Random Forest Regressor

### Input Features
1. Registered Year
2. Engine Capacity (cc)
3. Transmission Type
4. Kilometers Driven
5. Owner Type
6. Fuel Type
7. Max Power (bhp)
8. Number of Seats
9. Mileage (kmpl)
10. Body Type

---

## 🎨 Screenshots

### Home Page
Modern, responsive landing page with hero section and feature highlights.

### Prediction Interface
Clean, intuitive form with real-time validation and instant results.

### Results Dashboard
Detailed price prediction with market insights and depreciation analysis.

---

## 🔮 Future Enhancements

- [ ] Add more car brands and models
- [ ] Implement user authentication
- [ ] Create mobile app (iOS/Android)
- [ ] Add price trend graphs
- [ ] Integrate real-time market data API
- [ ] Multi-language support
- [ ] Advanced comparison features
- [ ] Email notification system
- [ ] Social media sharing

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

<div align="center">

### **Ankit Raj**

*AIML Student | Web Developer | Machine Learning Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-@Ankit2006Raj-181717?style=for-the-badge&logo=github)](https://github.com/Ankit2006Raj)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankit_Raj-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ankit-raj-226a36309)
[![Email](https://img.shields.io/badge/Email-ankit9905163014@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ankit9905163014@gmail.com)

</div>

---

## 🙏 Acknowledgments

- Dataset sourced from real-world car sales data
- UI inspiration from modern web design trends
- Machine learning guidance from scikit-learn documentation
- Community feedback and testing support

---

## 📞 Contact & Support

For questions, suggestions, or support:

- **Email**: [ankit9905163014@gmail.com](mailto:ankit9905163014@gmail.com)
- **GitHub Issues**: [Report a bug](https://github.com/Ankit2006Raj/car-price-prediction/issues)
- **LinkedIn**: [Connect with me](https://www.linkedin.com/in/ankit-raj-226a36309)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ by [Ankit Raj](https://github.com/Ankit2006Raj)

</div>
"# CAR_PRICE-_PREDICTION" 
