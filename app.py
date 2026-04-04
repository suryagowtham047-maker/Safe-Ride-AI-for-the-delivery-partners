from flask import Flask, render_template, request
import webbrowser
import threading
import sqlite3
import requests
import random
from ml_pricing import predict_premium_ai
from triggers import get_automated_disruptions, calculate_payouts

app = Flask(__name__)

import os
DB_PATH = '/tmp/database.db' if os.environ.get('VERCEL') else 'database.db'

# -------------------------------
# 📦 DATABASE SETUP
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            unique_id TEXT,
            email TEXT,
            name TEXT,
            location TEXT,
            policy TEXT,
            premium INTEGER,
            password TEXT,
            wallet_balance INTEGER DEFAULT 0
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount INTEGER,
            reason TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Graceful migrations
    for col in ['policy', 'password', 'wallet_balance', 'email', 'unique_id']:
        try:
            if col == 'wallet_balance':
                conn.execute(f"ALTER TABLE users ADD COLUMN {col} INTEGER DEFAULT 0")
            else:
                conn.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass
    conn.close()

init_db()

# -------------------------------
# 🏠 HOME PAGE
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        conn = sqlite3.connect(DB_PATH)
        user = conn.execute("SELECT unique_id, password FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if user:
            # Simulated Email Sending Output
            simulated_email = f"<b>Simulation: Email Sent!</b><br><br>To: {email}<br><br>Hello,<br>Your Unique ID is: <b>{user[0]}</b><br>Your Password is: <b>{user[1]}</b>"
            return render_template('forgot_password.html', message=simulated_email)
        else:
            return render_template('forgot_password.html', message="If an account exists for that email, recovery instructions have been sent.")
            
    return render_template('forgot_password.html')

@app.route('/login', methods=['POST'])
def login():
    unique_id = request.form.get('unique_id')
    password = request.form.get('password')
    conn = sqlite3.connect(DB_PATH)
    user = conn.execute("SELECT id FROM users WHERE unique_id = ? AND password = ?", (unique_id, password)).fetchone()
    conn.close()
    if user:
        from flask import redirect, url_for
        return redirect(url_for('dashboard', user_id=user[0]))
    return "Invalid Login Credentials! Go back and try again."

# -------------------------------
# 🧠 AI PREMIUM CALCULATION
# -------------------------------
# AI Premium logic is handled by ml_pricing.py

# -------------------------------
# 🌦️ WEATHER API
# -------------------------------
API_KEY = "YOUR_API_KEY"   # 🔑 PUT YOUR API KEY IN QUOTES

def get_weather():
    if API_KEY == "YOUR_API_KEY" or not API_KEY:
        # Avoid API ID error by using mock data if no key is supplied
        return random.randint(30, 45), random.choice(["Clear", "Rain", "Clouds", "Haze"])
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
        email = request.form['email']
        policy = request.form.get('policy', 'basic')
        return render_template('set_location.html', name=name, email=email, policy=policy)

    return render_template('register.html')

import string
@app.route('/set_location', methods=['POST'])
def set_location():
    name = request.form['name']
    email = request.form['email']
    policy = request.form['policy']
    location = request.form['location']

    risk_score = random.randint(1,5)
    premium = predict_premium_ai(location, risk_score, policy)

    # Generate unique ID
    unique_id = "SRA-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (unique_id, email, name, location, policy, premium) VALUES (?,?,?,?,?,?)",
                 (unique_id, email, name, location, policy, premium))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return render_template('set_password.html', user_id=user_id, unique_id=unique_id, name=name, premium=premium, policy=policy)

    return render_template('register.html')

@app.route('/save_password', methods=['POST'])
def save_password():
    user_id = request.form['user_id']
    password = request.form['password']
    name = request.form['name']
    premium = request.form['premium']
    policy = request.form['policy']

    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))
    conn.commit()
    conn.close()

    from flask import redirect, url_for
    return redirect(url_for('dashboard', user_id=user_id))

@app.route('/dashboard')
def dashboard():
    user_id = request.args.get('user_id')
    if not user_id:
        return "User ID missing"
        
    conn = sqlite3.connect(DB_PATH)
    user = conn.execute("SELECT name, premium, policy, wallet_balance FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return "User not found"
        
    claims = conn.execute("SELECT amount, reason, timestamp FROM claims WHERE user_id = ? ORDER BY timestamp DESC", (user_id,)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', user_id=user_id, name=user[0], premium=user[1], policy=user[2], wallet_balance=user[3], claims=claims)

# -------------------------------
# ⚡ ZERO TOUCH AUTO-TRIGGER SIMULATION
# -------------------------------
@app.route('/simulate_auto_check')
def simulate_auto_check():
    user_id = request.args.get('user_id')
    if not user_id:
        return {"status": "error", "message": "User ID missing"}
        
    conn = sqlite3.connect(DB_PATH)
    user = conn.execute("SELECT policy, wallet_balance FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if not user:
        return {"status": "error", "message": "User not found"}
        
    policy = user[0]
    
    temp, weather = get_weather()
    disruptions = get_automated_disruptions(temp, weather)
    payouts = calculate_payouts(disruptions, policy)
    
    total_payout = 0
    for p in payouts:
        total_payout += p["amount"]
        conn.execute("INSERT INTO claims (user_id, amount, reason) VALUES (?,?,?)", (user_id, p["amount"], p["reason"]))
        
    if total_payout > 0:
        conn.execute("UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?", (total_payout, user_id))
    
    conn.commit()
    conn.close()
    
    return {"status": "success", "payouts": payouts, "total": total_payout}

# -------------------------------
# 💳 PAYMENT GATEWAY SIMULATION
# -------------------------------
@app.route('/api/change_password', methods=['POST'])
def change_password():
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    if not user_id or not new_password:
        return {"status": "error", "message": "Missing credentials"}
        
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Password successfully updated!"}

@app.route('/payment_simulation')
def payment_simulation():
    # Simulates a payment gateway withdrawal of wallet funds
    user_id = request.args.get('user_id')
    upi = request.args.get('upi', 'unknown_upi')
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET wallet_balance = 0 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Funds successfully transferred to UPI ID: {upi}"}

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