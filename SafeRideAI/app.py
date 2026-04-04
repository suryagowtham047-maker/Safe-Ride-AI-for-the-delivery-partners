from flask import Flask, render_template, request
import webbrowser
import threading
import sqlite3
import requests
import random

app = Flask(__name__)

# -------------------------------
# 📦 DATABASE SETUP
# -------------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            premium INTEGER
        )
    ''')
    conn.close()

init_db()

# -------------------------------
# 🏠 HOME PAGE
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -------------------------------
# 🧠 AI PREMIUM CALCULATION
# -------------------------------
def calculate_premium(location, risk_score):
    base = 50
    if location == "high":
        base += 20
    elif location == "medium":
        base += 10
    return base + (risk_score * 10)

# -------------------------------
# 🌦️ WEATHER API
# -------------------------------
API_KEY = "YOUR_API_KEY"   # 🔑 PUT YOUR API KEY IN QUOTES

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        temp = data['main']['temp']
        weather = data['weather'][0]['main']

        return temp, weather
    except:
        return None, None

# -------------------------------
# 📝 REGISTRATION
# -------------------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']

        risk_score = random.randint(1,5)
        premium = calculate_premium(location, risk_score)

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO users (name, location, premium) VALUES (?,?,?)",
                     (name, location, premium))
        conn.commit()
        conn.close()

        return render_template('dashboard.html', name=name, premium=premium)

    return render_template('register.html')

# -------------------------------
# ⚡ CLAIM TRIGGER
# -------------------------------
@app.route('/check')
def check():
    temp, weather = get_weather()

    if temp is None:
        return "❌ Weather API error"

    if "Rain" in weather:
        return "💰 Rain Claim → ₹200 Credited"
    elif temp > 40:
        return "💰 Heat Claim → ₹150 Credited"
    else:
        return f"✅ Safe ({weather}, {temp}°C)"

# -------------------------------
# 🌐 AUTO OPEN BROWSER
# -------------------------------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# -------------------------------
# ▶️ RUN SERVER
# -------------------------------
if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)