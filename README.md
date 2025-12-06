# 🛡️ Phishing Website Detection using Machine Learning

A machine learning-based web application that classifies URLs as **phishing** or **legitimate** using URL features, domain information, and statistical patterns. This project helps improve user cybersecurity by detecting malicious URLs in real-time.

---

## 🚀 Features

- Web-based tool built using **Flask**
- Real-time URL classification (Phishing / Legitimate)
- Extracts 20+ URL & domain-level features
- Uses **Random Forest** and **XGBoost** models
- Achieves **83% accuracy**
- MySQL backend for storing predictions
- Clean UI for easy user interaction

---

## 📂 Dataset Sources

This project uses open-source datasets:

- **PhishTank** (Phishing URLs)  
- **Alexa Top Sites** (Legitimate URLs)

Data is cleaned and combined using **Pandas** and **NumPy**.

---

## 🧠 Machine Learning Workflow

1. **Data Collection** from PhishTank & Alexa  
2. **Feature Engineering**  
   - SSL certificate validation  
   - Domain age extraction  
   - “@” symbol, special character checks  
   - URL/IP-based analysis  
3. **EDA & Visualization** using Matplotlib + Seaborn  
4. **Model Training**  
   - Random Forest  
   - XGBoost  
5. **Hyperparameter Tuning**  
6. **Web Deployment** using Flask + MySQL  
7. **Real-time URL Prediction**

---

## 📊 Model Performance

- **Accuracy:** 83%  
- Feature importance analyzed using tree-based models  
- Balanced evaluation across phishing & legitimate samples  

---

## 🛠️ Tech Stack

**Languages:** Python, HTML, CSS  
**ML:** Scikit-learn, XGBoost  
**Data:** Pandas, NumPy  
**Visualization:** Matplotlib, Seaborn  
**Web Framework:** Flask  
**Database:** MySQL  
**Others:** whois, requests, ipaddress  

---

## ▶️ How to Run the Project (Locally)

```bash
# Clone repository
git clone https://github.com/yourusername/phishing-detection-ml.git
cd phishing-detection-ml

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
