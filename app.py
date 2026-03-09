"""
MathBlitz - Production-Ready Practice App
=========================================
"""

import streamlit as st
import random
import time
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# ==================== CONFIG ====================
st.set_page_config(page_title="MathBlitz", page_icon="🎮", layout="wide", 
    menu_items={"About": "MathBlitz - Master math skills!"})

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
SOUNDS_DIR = APP_DIR / "Sounds"
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "progress").mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"

DIFFICULTY_SETTINGS = {
    "Easy": {"time_limit": 60, "points_multiplier": 1},
    "Medium": {"time_limit": 45, "points_multiplier": 2},
    "Hard": {"time_limit": 30, "points_multiplier": 3}
}

# ==================== LEADERBOARD ====================
LEADERBOARD_FILE = DATA_DIR / "leaderboard.json"

def load_leaderboard():
    if LEADERBOARD_FILE.exists():
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leaderboard_entry(username, score):
    leaderboard = load_leaderboard()
    for entry in leaderboard:
        if entry['username'] == username:
            if score > entry['score']:
                entry['score'] = score
            entry['last_update'] = datetime.now().isoformat()
            break
    else:
        leaderboard.append({'username': username, 'score': score, 'last_update': datetime.now().isoformat()})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:100]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)
    return leaderboard

def get_share_text(score, streak):
    return f"🎉 I just scored {score} points with a {streak} streak on MathBlitz! 💵🧮 Play now: https://mathblitz.streamlit.app #MathBlitz #MathSkills"

SERVICES = {"Milk Delivery": 30, "Newspaper": 5, "Water Can": 20, "Laundry": 50, "Gardening": 40, "Internet": 35}

# ==================== SOUND ====================
def play_sound(sound_name):
    if not st.session_state.get("settings", {}).get("sound_enabled", True):
        return
    try:
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        sound_files = {"correct": SOUNDS_DIR / "correct.wav", "wrong": SOUNDS_DIR / "wrong.wav", "new_task": SOUNDS_DIR / "new_task.wav"}
        sf = sound_files.get(sound_name)
        if sf and sf.exists():
            pygame.mixer.music.load(str(sf))
            pygame.mixer.music.play()
    except:
        pass

# ==================== AUTH ====================
import hashlib
import secrets

def hash_password(password):
    """Hash a password using SHA-256 with a random salt"""
    salt = secrets.token_hex(16)
    password_with_salt = salt + password
    hashed = hashlib.sha256(password_with_salt.encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password, stored_hash):
    """Verify a password against a stored hash"""
    try:
        salt, hashed = stored_hash.split('$')
        password_with_salt = salt + password
        new_hash = hashlib.sha256(password_with_salt.encode()).hexdigest()
        return new_hash == hashed
    except:
        return False

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    # Hash the password before storing
    hashed_password = hash_password(password)
    users[username] = {"password": hashed_password, "created_at": datetime.now().isoformat()}
    save_users(users)
    return True, "Registration successful"

def verify_user(username, password):
    users = load_users()
    if username in users:
        stored_hash = users[username]["password"]
        return verify_password(password, stored_hash)
    return False

# ==================== PROGRESS ====================
def get_progress_file(username):
    return DATA_DIR / "progress" / f"{username}.csv"

def load_user_progress(username):
    pf = get_progress_file(username)
    if pf.exists():
        return pd.read_csv(pf)
    return pd.DataFrame(columns=["Timestamp", "Mode", "Exercise", "Difficulty", "UserAnswer", "CorrectAnswer", "Status", "TimeTaken", "Points"])

def load_user_score(username):
    p = load_user_progress(username)
    return int(p["Points"].sum()) if not p.empty else 0

def load_user_streak(username):
    p = load_user_progress(username)
    if p.empty: return 0
    return len(p[p["Status"] == "Correct"].tail(10))

def save_user_progress(username, entry):
    pf = get_progress_file(username)
    df = load_user_progress(username)
    new_df = pd.DataFrame([entry])
    if df.empty:
        new_df.to_csv(pf, index=False)
    else:
        pd.concat([df, new_df], ignore_index=True).to_csv(pf, index=False)

def reset_user_progress(username):
    pf = get_progress_file(username)
    if pf.exists(): pf.unlink()

def delete_user_account(username):
    # Delete user from users.json
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
    
    # Delete user progress file
    pf = get_progress_file(username)
    if pf.exists():
        pf.unlink()
    
    # Remove from leaderboard
    leaderboard = load_leaderboard()
    leaderboard = [entry for entry in leaderboard if entry['username'] != username]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

# ==================== SETTINGS ====================
def load_settings(username):
    users = load_users()
    if username in users and "settings" in users[username]:
        return users[username]["settings"]
    return {"sound_enabled": True, "default_difficulty": "Medium", "default_exercise": "Cash Counting"}

def save_settings(username, settings):
    users = load_users()
    if username in users:
        users[username]["settings"] = settings
        save_users(users)

# ==================== EXERCISES ====================
FORMULAS = {
    "Cash Counting": {"icon": "🎮", "formula": "Change = Paid - Price", "example": "Price: $45, Paid: $50 → Change = $50 - $45 = $5", "tip": "Subtract the price from the amount paid"},
    "Billing Calculation": {"icon": "🧾", "formula": "Amount = (Total Days - Missed Days) × Daily Cost", "example": "30 days claimed, 5 missed, $20/day → (30-5) × $20 = $500", "tip": "First subtract missed days, then multiply by daily rate"},
    "Tip Calculator": {"icon": "🍽️", "formula": "Tip = Bill × (Tip% ÷ 100)", "example": "$100 bill, 15% tip → $100 × 0.15 = $15", "tip": "Move decimal 1 place left for 10%, double for 20%"},
    "Discount Calculator": {"icon": "🏷️", "formula": "Final = Original × (100 - Discount%) ÷ 100", "example": "$80 item, 25% off → $80 × 0.75 = $60", "tip": "Calculate discount amount first, subtract from original"},
    "Tax Calculator": {"icon": "🧾", "formula": "Tax = Price × (Tax% ÷ 100)", "example": "$50 item, 8% tax → $50 × 0.08 = $4", "tip": "Multiply price by tax rate as decimal"},
    "Split Bill": {"icon": "👥", "formula": "Per Person = (Total + Tip) ÷ People", "example": "$100 bill, 20% tip, 4 people → ($100 × 1.20) ÷ 4 = $30", "tip": "Add tip to total first, then divide by number of people"},
    "Profit/Loss": {"icon": "📈", "formula": "Profit = Cost × Markup%", "example": "$80 cost, 25% markup → $80 × 0.25 = $20 profit", "tip": "Profit = Selling Price - Cost Price"},
    "Unit Price Compare": {"icon": "⚖️", "formula": "Unit Price = Price ÷ Quantity", "example": "$10 for 5 items = $2/item", "tip": "Calculate price per item for each option, lower is better"},
    "Percentage": {"icon": "🔢", "formula": "Result = Number × (Percentage ÷ 100)", "example": "20% of 150 → 150 × 0.20 = 30", "tip": "Multiply number by percentage as decimal"},
    "Currency Convert": {"icon": "💱", "formula": "Result = Amount × Exchange Rate", "example": "$100 to EUR (0.85 rate) = $85 EUR", "tip": "Multiply amount by the conversion rate"},
    "Simple Interest": {"icon": "📊", "formula": "Interest = Principal × Rate × Time ÷ 100", "example": "$1000 at 5% for 2 years = $100 interest", "tip": "Principal × Rate × Years, then divide by 100"}
}

def generate_task(exercise, difficulty):
    if exercise == "Cash Counting":
        price = random.randint(1, 50 if difficulty == "Easy" else 200 if difficulty == "Medium" else 500)
        paid = price + random.randint(1, 20 if difficulty == "Easy" else 50 if difficulty == "Medium" else 100)
        return {"exercise": "Cash Counting", "icon": "🎮", "type": "cash", "price": price, "paid": paid, "correct_answer": paid - price}
    elif exercise == "Billing Calculation":
        service = random.choice(list(SERVICES.keys()))
        daily = SERVICES[service]
        total = random.randint(10, 20) if difficulty == "Easy" else random.randint(20, 31) if difficulty == "Medium" else random.randint(25, 60)
        missed = random.randint(0, 2) if difficulty == "Easy" else random.randint(0, 4) if difficulty == "Medium" else random.randint(1, 8)
        return {"exercise": "Billing Calculation", "icon": "🧾", "type": "billing", "service": service, "total_days": total, "missed_days": missed, "daily_cost": daily, "correct_answer": (total - missed) * daily}
    elif exercise == "Tip Calculator":
        bill = random.randint(20, 100) if difficulty == "Easy" else random.randint(50, 300) if difficulty == "Medium" else random.randint(100, 1000)
        tip = random.choice([10, 15, 18, 20, 25])
        return {"exercise": "Tip Calculator", "icon": "🍽️", "type": "tip", "bill": bill, "tip_percent": tip, "correct_answer": round(bill * tip / 100, 2)}
    elif exercise == "Discount Calculator":
        price = random.randint(50, 200) if difficulty == "Easy" else random.randint(100, 500) if difficulty == "Medium" else random.randint(200, 2000)
        disc = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
        return {"exercise": "Discount Calculator", "icon": "🏷️", "type": "discount", "original_price": price, "discount_percent": disc, "correct_answer": round(price * (100 - disc) / 100, 2)}
    elif exercise == "Tax Calculator":
        price = random.randint(50, 200) if difficulty == "Easy" else random.randint(100, 500) if difficulty == "Medium" else random.randint(200, 2000)
        tax = random.choice([5, 7, 8, 10, 12, 15])
        return {"exercise": "Tax Calculator", "icon": "🧾", "type": "tax", "price": price, "tax_rate": tax, "correct_answer": round(price * tax / 100, 2)}
    elif exercise == "Split Bill":
        total = random.randint(30, 150) if difficulty == "Easy" else random.randint(50, 300) if difficulty == "Medium" else random.randint(100, 1000)
        people = random.randint(2, 4) if difficulty == "Easy" else random.randint(2, 6) if difficulty == "Medium" else random.randint(2, 10)
        tip = random.choice([0, 10, 15, 20])
        return {"exercise": "Split Bill", "icon": "👥", "type": "split", "total": total, "people": people, "tip": tip, "correct_answer": round(total * (100 + tip) / 100 / people, 2)}
    elif exercise == "Profit/Loss":
        cost = random.randint(20, 100) if difficulty == "Easy" else random.randint(50, 300) if difficulty == "Medium" else random.randint(100, 1000)
        markup = random.randint(10, 50)
        return {"exercise": "Profit/Loss", "icon": "📈", "type": "profit", "cost_price": cost, "markup_percent": markup, "correct_answer": round(cost * markup, 2)}
    elif exercise == "Unit Price Compare":
        if difficulty == "Easy":
            p1, q1 = random.randint(10, 50), random.randint(2, 5)
            p2, q2 = random.randint(10, 50), random.randint(2, 5)
        elif difficulty == "Medium":
            p1, q1 = random.randint(20, 100), random.randint(3, 8)
            p2, q2 = random.randint(20, 100), random.randint(3, 8)
        else:
            p1, q1 = random.randint(50, 200), random.randint(5, 12)
            p2, q2 = random.randint(50, 200), random.randint(5, 12)
        u1, u2 = p1/q1, p2/q2
        return {"exercise": "Unit Price Compare", "icon": "⚖️", "type": "unit", "price1": p1, "qty1": q1, "price2": p2, "qty2": q2, "correct_answer": 1 if u1 < u2 else 2, "unit1": round(u1,2), "unit2": round(u2,2)}
    elif exercise == "Percentage":
        if difficulty == "Easy":
            num = random.randint(10, 100)
            pct = random.choice([10, 20, 25, 50, 75])
        elif difficulty == "Medium":
            num = random.randint(50, 500)
            pct = random.randint(5, 50)
        else:
            num = random.randint(100, 1000)
            pct = random.randint(1, 75)
        return {"exercise": "Percentage", "icon": "🔢", "type": "percent", "number": num, "percent": pct, "correct_answer": round(num * pct / 100, 2)}
    elif exercise == "Currency Convert":
        currencies = [("USD", {"EUR": 0.85, "GBP": 0.73, "JPY": 110, "INR": 74, "CAD": 1.25}), ("EUR", {"USD": 1.18, "GBP": 0.86, "JPY": 130, "INR": 87, "CAD": 1.47}), ("GBP", {"USD": 1.37, "EUR": 1.16, "JPY": 150, "INR": 101, "CAD": 1.71}), ("INR", {"USD": 0.012, "EUR": 0.011, "GBP": 0.0099, "JPY": 1.5, "CAD": 0.017})]
        base = random.choice(currencies)
        base_currency, rates = base[0], base[1]
        target = random.choice(list(rates.keys()))
        amount = random.randint(10, 100) if difficulty == "Easy" else random.randint(50, 500) if difficulty == "Medium" else random.randint(100, 2000)
        rate = rates[target]
        return {"exercise": "Currency Convert", "icon": "💱", "type": "currency", "from_currency": base_currency, "to_currency": target, "amount": amount, "rate": rate, "correct_answer": round(amount * rate, 2)}
    elif exercise == "Simple Interest":
        principal = random.randint(100, 1000) if difficulty == "Easy" else random.randint(500, 5000) if difficulty == "Medium" else random.randint(1000, 20000)
        rate = random.randint(5, 15)
        years = random.randint(1, 3) if difficulty == "Easy" else random.randint(1, 5) if difficulty == "Medium" else random.randint(1, 10)
        return {"exercise": "Simple Interest", "icon": "📊", "type": "interest", "principal": principal, "rate": rate, "years": years, "correct_answer": round(principal * rate * years / 100, 2)}
    else:
        price = random.randint(1, 50)
        paid = price + random.randint(1, 20)
        return {"exercise": "Cash Counting", "icon": "🎮", "type": "cash", "price": price, "paid": paid, "correct_answer": paid - price}

EXERCISES = [("Cash Counting", "🎮"), ("Billing Calculation", "🧾"), ("Tip Calculator", "🍽️"), ("Discount Calculator", "🏷️"), ("Tax Calculator", "🧾"), ("Split Bill", "👥"), ("Profit/Loss", "📈"), ("Unit Price Compare", "⚖️"), ("Percentage", "🔢"), ("Currency Convert", "💱"), ("Simple Interest", "📊")]
EXERCISE_NAMES = [e[0] for e in EXERCISES]

# ==================== CSS ====================
def custom_css():
    st.markdown("""<style>
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); min-height: 100vh; }
    .main-title { font-size: 3.5rem !important; font-weight: 900 !important; background: linear-gradient(90deg, #00d4ff, #7b2ff7, #f107a3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .card { background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); backdrop-filter: blur(20px); border-radius: 20px; padding: 25px; margin: 15px 0; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
    .task-display { background: linear-gradient(145deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 100%); backdrop-filter: blur(20px); border-radius: 30px; padding: 40px; text-align: center; margin: 25px 0; border: 2px solid rgba(255,255,255,0.15); box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
    .task-entrance { animation: flashcardFlip 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    @keyframes flashcardFlip { 0% { opacity: 0; transform: perspective(1000px) rotateX(-15deg) rotateY(30deg) translateY(50px) scale(0.9); } 50% { opacity: 0.8; transform: perspective(1000px) rotateX(5deg) rotateY(-5deg) translateY(10px) scale(0.98); } 100% { opacity: 1; transform: perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1); } }
    .stButton > button { border-radius: 20px !important; padding: 15px 30px !important; font-weight: 700 !important; font-size: 1.1rem !important; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important; }
    .stButton > button:hover { transform: translateY(-4px) scale(1.02) !important; box-shadow: 0 15px 40px rgba(123, 47, 247, 0.4) !important; }
    .primary-btn > button { background: linear-gradient(135deg, #7b2ff7 0%, #f107a3 100%) !important; border: none !important; color: white !important; }
    .success-msg { background: linear-gradient(135deg, #00b09b, #96c93d); padding: 25px; border-radius: 20px; text-align: center; font-size: 1.6rem; color: white; animation: slideIn 0.3s; }
    .error-msg { background: linear-gradient(135deg, #eb3349, #f45c43); padding: 25px; border-radius: 20px; text-align: center; font-size: 1.6rem; color: white; animation: shake 0.3s; }
    .formula-box { background: linear-gradient(145deg, rgba(123, 47, 247, 0.2) 0%, rgba(0, 212, 255, 0.1) 100%); border-radius: 15px; padding: 20px; margin: 10px 0; border-left: 4px solid #7b2ff7; }
    .formula-title { color: #00d4ff; font-size: 1.1rem; font-weight: bold; }
    .formula-text { color: white; font-size: 1.3rem; font-family: 'Courier New', monospace; text-align: center; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 10px; margin: 10px 0; }
    .exercise-icon { font-size: 5rem; text-align: center; display: block; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .stat-card { background: linear-gradient(145deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%); border-radius: 18px; padding: 20px; text-align: center; color: white; }
    .stat-card h2 { font-size: 2.5rem !important; margin: 5px 0 !important; }
    .leaderboard-card { background: linear-gradient(145deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%); backdrop-filter: blur(20px); border-radius: 20px; padding: 20px; margin: 15px 0; }
    .leaderboard-title { color: #00d4ff; font-size: 1.3rem; font-weight: bold; text-align: center; margin-bottom: 15px; }
    .leaderboard-item { display: flex; justify-content: space-between; padding: 10px 15px; margin: 8px 0; border-radius: 10px; background: rgba(255,255,255,0.05); }
    .leaderboard-item.top-1 { background: linear-gradient(90deg, #ffd700, #ffaa00); }
    .leaderboard-item.top-2 { background: linear-gradient(90deg, #c0c0c0, #a0a0a0); }
    .leaderboard-item.top-3 { background: linear-gradient(90deg, #cd7f32, #b87333); }
    .lb-rank { font-weight: bold; width: 30px; }
    .lb-name { flex: 1; color: white; }
    .lb-score { font-weight: bold; color: #00d4ff; }
    .calc-breakdown { background: linear-gradient(145deg, rgba(0,212,255,0.1) 0%, rgba(123,47,247,0.1) 100%); border-radius: 15px; padding: 20px; margin: 15px 0; border-left: 4px solid #00d4ff; }
    .calc-title { color: #00d4ff; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px; }
    .calc-step { color: white; font-family: 'Courier New', monospace; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .calc-result { color: #00b09b; font-size: 1.2rem; font-weight: bold; margin-top: 10px; }
    .share-container { display: flex; gap: 10px; justify-content: center; margin: 15px 0; }
    .share-btn { padding: 10px 20px; border-radius: 25px; color: white; text-decoration: none; font-weight: bold; transition: transform 0.3s; }
    .share-btn:hover { transform: scale(1.1); }
    .share-x { background: #000; }
    .share-fb { background: #1877f2; }
    .share-whatsapp { background: #25d366; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(15,12,41,0.95) 0%, rgba(48,43,99,0.95) 100%) !important; }
    .sidebar-title { font-size: 1.8rem; font-weight: bold; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; padding: 15px; }
    .sidebar-score { display: flex; justify-content: space-around; padding: 15px; margin: 10px 0; background: rgba(255,255,255,0.05); border-radius: 15px; }
    .score-item { text-align: center; }
    .score-item .number { font-size: 1.8rem; font-weight: bold; color: #00d4ff; }
    .score-item .label { font-size: 0.8rem; color: rgba(255,255,255,0.6); }
    .stNumberInput > div > div > input { background: rgba(255,255,255,0.1) !important; border: 2px solid rgba(255,255,255,0.2) !important; border-radius: 12px !important; color: white !important; font-size: 1.2rem !important; }
    .stSelectbox > div > div > div { background: rgba(255,255,255,0.1) !important; border-radius: 12px !important; }
    @keyframes slideIn { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-5px); } 75% { transform: translateX(5px); } }
    
    /* Time's Up Popup Styles */
    .times-up-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: 9998;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .times-up-popup {
        background: linear-gradient(145deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        border: 3px solid #ef4444;
        box-shadow: 0 20px 60px rgba(239, 68, 68, 0.5);
        text-align: center;
        max-width: 90%;
        animation: popIn 0.3s ease;
    }
    @keyframes popIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    .times-up-title {
        font-size: 3rem;
        font-weight: bold;
        color: #ef4444;
        animation: pulse 1s infinite;
        margin-bottom: 20px;
    }
    .times-up-message {
        color: white;
        font-size: 1.2rem;
        margin: 15px 0;
    }
    .times-up-buttons {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin-top: 25px;
        flex-wrap: wrap;
    }
    .times-up-btn {
        padding: 15px 30px !important;
        border-radius: 15px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border: none !important;
        cursor: pointer;
        transition: all 0.3s !important;
    }
    .continue-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
    }
    .continue-btn:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4) !important;
    }
    .next-task-btn {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
    }
    .next-task-btn:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Difficulty Selection Styles */
    .difficulty-container {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin: 10px 0;
    }
    .difficulty-btn {
        padding: 12px 25px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        border: 2px solid transparent !important;
        cursor: pointer;
        transition: all 0.3s ease !important;
        opacity: 0.7;
    }
    .difficulty-btn.selected {
        opacity: 1;
        transform: scale(1.05);
    }
    .difficulty-btn.easy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border-color: #10b981 !important;
    }
    .difficulty-btn.easy.selected {
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.6) !important;
    }
    .difficulty-btn.medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: white !important;
        border-color: #f59e0b !important;
    }
    .difficulty-btn.medium.selected {
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.6) !important;
    }
    .difficulty-btn.hard {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border-color: #ef4444 !important;
    }
    .difficulty-btn.hard.selected {
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.6) !important;
    }
    
    /* Activity Title Style */
    .activity-title {
        background: linear-gradient(90deg, #7b2ff7, #f107a3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 8px;
    }
    
    @media (max-width: 768px) {
        .stApp { padding: 10px; }
        .main-title { font-size: 2rem !important; }
        .task-display { padding: 20px !important; border-radius: 20px !important; }
        .exercise-icon { font-size: 3rem !important; }
        .stButton > button { padding: 12px 20px !important; font-size: 1rem !important; min-height: 50px; }
        .card { padding: 15px !important; border-radius: 15px !important; }
        .stat-card { padding: 15px !important; }
        .stat-card h2 { font-size: 1.5rem !important; }
        .sidebar-title { font-size: 1.3rem !important; }
        .success-msg, .error-msg { font-size: 1.2rem !important; padding: 15px !important; }
        .share-container { flex-wrap: wrap; }
        .share-btn { padding: 8px 15px; font-size: 0.9rem; }
        .times-up-popup { padding: 25px; }
        .times-up-title { font-size: 2rem; }
        .times-up-buttons { flex-direction: column; }
        .difficulty-container { flex-wrap: wrap; }
    }
    @media (max-width: 480px) {
        .main-title { font-size: 1.8rem !important; }
        .task-display { padding: 15px !important; }
        .exercise-icon { font-size: 2.5rem !important; }
        .task-question { font-size: 1.1rem !important; }
    }
    input, select, textarea { font-size: 16px !important; }
    button { user-select: none !important; -webkit-tap-highlight-color: transparent; }
    </style>""", unsafe_allow_html=True)

def login_page():
    custom_css()
    
    # Check if showing legal pages
    if st.session_state.get("show_privacy_policy"):
        show_privacy_policy_page()
        return
    if st.session_state.get("show_terms_of_service"):
        show_terms_of_service_page()
        return
    
    st.markdown('<p class="main-title">💵 MathBlitz</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color: rgba(255,255,255,0.7); font-size: 1.3rem;">Master math skills with interactive exercises! 🧮</p>', unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        with tab1:
            with st.form("login"):
                username = st.text_input("👤 Username", placeholder="Enter username")
                password = st.text_input("🔐 Password", type="password", placeholder="Enter password")
                if st.form_submit_button("🚀 Login", use_container_width=True):
                    if verify_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.score = load_user_score(username)
                        st.session_state.streak = load_user_streak(username)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
        with tab2:
            with st.form("register"):
                new_user = st.text_input("👤 New Username", placeholder="Choose username")
                new_pass = st.text_input("🔐 New Password", type="password", placeholder="Choose password")
                confirm = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
                if st.form_submit_button("📝 Register", use_container_width=True):
                    if new_pass != confirm:
                        st.error("❌ Passwords don't match")
                    elif len(new_user) < 3:
                        st.error("❌ Username too short")
                    elif len(new_pass) < 4:
                        st.error("❌ Password too short")
                    else:
                        success, msg = register_user(new_user, new_pass)
                        if success:
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error(f"❌ {msg}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Legal links at bottom - centered side by side
    col_legal1, col_legal2, col_legal3 = st.columns([1, 2, 1])
    with col_legal2:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Privacy Policy", key="priv_btn", use_container_width=True):
                st.session_state.show_privacy_policy = True
                st.rerun()
        with c2:
            if st.button("Terms of Service", key="tos_btn", use_container_width=True):
                st.session_state.show_terms_of_service = True
                st.rerun()

def sidebar():
    custom_css()
    with st.sidebar:
        st.markdown(f'<p class="sidebar-title">👤 {st.session_state.username}</p>', unsafe_allow_html=True)
        st.markdown(f'''<div class="sidebar-score">
            <div class="score-item"><div class="number">🏆 {st.session_state.score}</div><div class="label">Score</div>
            <div class="score-item"><div class="number">🔥 {st.session_state.streak}</div><div class="label">Streak</div>
        </div>''', unsafe_allow_html=True)
        st.markdown('<div class="leaderboard-card"><div class="leaderboard-title">🌍 World Leaderboard</div>', unsafe_allow_html=True)
        leaderboard = load_leaderboard()[:10]
        for i, entry in enumerate(leaderboard):
            rank_class = f"top-{i+1}" if i < 3 else ""
            is_current = entry["username"] == st.session_state.username
            name_display = entry["username"] + " (You)" if is_current else entry["username"]
            st.markdown(f'''<div class="leaderboard-item {rank_class}">
                <span class="lb-rank">#{i+1}</span>
                <span class="lb-name">{name_display}</span>
                <span class="lb-score">{entry["score"]}</span>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        menu_options = [("🎮 Practice", "practice"), ("📊 Progress", "progress"), ("⚙️ Settings", "settings")]
        selected = st.radio("menu", [m[0] for m in menu_options], label_visibility="collapsed")
        st.markdown("---")
        
        # Delete Account option with 2-step confirmation
        if "delete_confirm" not in st.session_state:
            st.session_state.delete_confirm = False
        if "delete_step" not in st.session_state:
            st.session_state.delete_step = 0
        
        if st.session_state.delete_confirm:
            # Step 2: Final confirmation
            st.warning(f"⚠️ Type '{st.session_state.username}' to confirm delete:")
            confirm_text = st.text_input("Enter username to confirm", key="confirm_delete_input")
            col_del1, col_del2 = st.columns(2)
            with col_del1:
                if st.button("✅ Confirm Delete", use_container_width=True):
                    if confirm_text == st.session_state.username:
                        delete_user_account(st.session_state.username)
                        st.session_state.logged_in = False
                        st.session_state.delete_confirm = False
                        st.session_state.delete_step = 0
                        st.success("✅ Account deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Username doesn't match")
            with col_del2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.delete_confirm = False
                    st.session_state.delete_step = 0
                    st.rerun()
        else:
            if st.button("🗑️ Delete Account", use_container_width=True):
                st.session_state.delete_confirm = True
                st.session_state.delete_step = 1
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        return selected.split()[0]

def show_calculation_breakdown(task):
    calc_html = '<div class="calc-breakdown"><div class="calc-title">📝 Calculation Breakdown</div>'
    if task["type"] == "cash":
        calc_html += f'<div class="calc-step">Step 1: Price = ${task["price"]}</div><div class="calc-step">Step 2: Paid = ${task["paid"]}</div><div class="calc-step">Step 3: Change = ${task["paid"]} - ${task["price"]}</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "billing":
        calc_html += f'<div class="calc-step">Step 1: Total days claimed = {task["total_days"]}</div><div class="calc-step">Step 2: Missed days = {task["missed_days"]}</div><div class="calc-step">Step 3: Actual days = {task["total_days"]} - {task["missed_days"]} = {task["total_days"] - task["missed_days"]}</div><div class="calc-step">Step 4: Amount = {task["total_days"] - task["missed_days"]} × ${task["daily_cost"]}</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "tip":
        calc_html += f'<div class="calc-step">Step 1: Bill = ${task["bill"]}</div><div class="calc-step">Step 2: Tip = {task["tip_percent"]}%</div><div class="calc-step">Step 3: Tip = ${task["bill"]} × {task["tip_percent"]/100}</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "discount":
        calc_html += f'<div class="calc-step">Step 1: Original = ${task["original_price"]}</div><div class="calc-step">Step 2: Discount = {task["discount_percent"]}%</div><div class="calc-step">Step 3: Final = ${task["original_price"]} × {100-task["discount_percent"]}/100</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "tax":
        calc_html += f'<div class="calc-step">Step 1: Price = ${task["price"]}</div><div class="calc-step">Step 2: Tax = {task["tax_rate"]}%</div><div class="calc-step">Step 3: Tax = ${task["price"]} × {task["tax_rate"]/100}</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "split":
        calc_html += f'<div class="calc-step">Step 1: Total = ${task["total"]}</div><div class="calc-step">Step 2: Tip = {task["tip"]}%</div><div class="calc-step">Step 3: People = {task["people"]}</div><div class="calc-step">Step 4: Per person = ${task["total"]} × (100+{task["tip"]})/100 ÷ {task["people"]}</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "profit":
        calc_html += f'<div class="calc-step">Step 1: Cost = ${task["cost_price"]}</div><div class="calc-step">Step 2: Markup = {task["markup_percent"]}%</div><div class="calc-step">Step 3: Profit = ${task["cost_price"]} × {task["markup_percent"]/100}</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    elif task["type"] == "unit":
        calc_html += f'<div class="calc-step">Option 1: ${task["price1"]} ÷ {task["qty1"]} = ${task["unit1"]}/item</div><div class="calc-step">Option 2: ${task["price2"]} ÷ {task["qty2"]} = ${task["unit2"]}/item</div><div class="calc-result">✓ Better option: {task["correct_answer"]}</div>'
    elif task["type"] == "percent":
        calc_html += f'<div class="calc-step">Step 1: Number = {task["number"]}</div><div class="calc-step">Step 2: {task["percent"]}% of {task["number"]}</div><div class="calc-step">Step 3: {task["number"]} × {task["percent"]/100}</div><div class="calc-result">✓ Answer: {task["correct_answer"]}</div>'
    elif task["type"] == "currency":
        calc_html += f'<div class="calc-step">Step 1: {task["amount"]} {task["from_currency"]}</div><div class="calc-step">Step 2: Rate = {task["rate"]}</div><div class="calc-step">Step 3: {task["amount"]} × {task["rate"]}</div><div class="calc-result">✓ Answer: {task["correct_answer"]} {task["to_currency"]}</div>'
    elif task["type"] == "interest":
        calc_html += f'<div class="calc-step">Step 1: Principal = ${task["principal"]}</div><div class="calc-step">Step 2: Rate = {task["rate"]}%</div><div class="calc-step">Step 3: Years = {task["years"]}</div><div class="calc-step">Step 4: ${task["principal"]} × {task["rate"]} × {task["years"]} ÷ 100</div><div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'
    calc_html += '</div>'
    return calc_html

def show_share_buttons(score, streak):
    share_text = get_share_text(score, streak)
    encoded_text = share_text.replace(" ", "%20").replace("!", "%21").replace("#", "%23")
    html = '<div class="share-container">'
    html += f'<a href="https://twitter.com/intent/tweet?text={encoded_text}" target="_blank" class="share-btn share-x">𝕏 Post</a>'
    html += f'<a href="https://www.facebook.com/sharer/sharer.php?u=https://mathblitz.streamlit.app&quote={encoded_text}" target="_blank" class="share-btn share-fb">f Facebook</a>'
    html += f'<a href="https://wa.me/?text={encoded_text}" target="_blank" class="share-btn share-whatsapp">📱 WhatsApp</a>'
    html += '</div>'
    return html

def show_formula(exercise):
    if exercise in FORMULAS:
        f = FORMULAS[exercise]
        st.markdown(f'''<div class="formula-box">
            <div class="formula-title">📐 {f["icon"]} Formula</div>
            <div class="formula-text">{f["formula"]}</div>
            <div class="formula-example">💡 Example: {f["example"]}</div>
            <div style="color: #f107a3; font-size: 0.9rem; margin-top: 8px;">✨ {f["tip"]}</div>''', unsafe_allow_html=True)

def exercise_page():
    custom_css()
    settings = st.session_state.get("settings", {})
    col1, col2, col3 = st.columns([2,2,1])
    with col1:
        exercise_idx = list(EXERCISE_NAMES).index(settings.get("default_exercise", "Cash Counting"))
        exercise = st.selectbox("🎯 Exercise", EXERCISE_NAMES, index=exercise_idx, label_visibility="collapsed")
    with col2:
        diff_idx = ["Easy", "Medium", "Hard"].index(settings.get("default_difficulty", "Medium"))
        difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"], index=diff_idx, label_visibility="collapsed")
    with col3:
        time_limit = DIFFICULTY_SETTINGS[difficulty]["time_limit"]
        if "start_time" in st.session_state:
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, time_limit - elapsed)
            color = "#00b09b" if remaining > 20 else "#f59e0b" if remaining > 10 else "#ef4444"
            st.markdown(f'<div style="text-align:center; padding: 12px; background: {color}; border-radius: 12px; color: white; font-weight: bold; font-size: 1.1rem;">⏱️ {int(remaining)}s</div>', unsafe_allow_html=True)
            if remaining <= 0 and not st.session_state.get("task_submitted", False):
                entry = {"Timestamp": datetime.now().isoformat(), "Mode": exercise, "Exercise": exercise, "Difficulty": difficulty, "UserAnswer": 0, "CorrectAnswer": 0, "Status": "Timeout", "TimeTaken": time_limit, "Points": 0}
                save_user_progress(st.session_state.username, entry)
                st.rerun()
    st.markdown("---")
    show_formula(exercise)
    if st.button("🎲 New Task" if not st.session_state.get("current_task") else "🔄 Next Task", type="primary", use_container_width=True):
        st.session_state.task_key = st.session_state.get("task_key", 0) + 1
        st.session_state.current_task = generate_task(exercise, difficulty)
        st.session_state.start_time = time.time()
        st.session_state.task_submitted = False
        st.session_state.show_result = False
        play_sound("new_task")
        st.rerun()
    if st.session_state.get("show_result", False):
        if "result_time" not in st.session_state:
            st.session_state.result_time = time.time()
        elapsed = time.time() - st.session_state.result_time
        if elapsed >= 2:
            st.session_state.current_task = generate_task(exercise, difficulty)
            st.session_state.start_time = time.time()
            st.session_state.task_submitted = False
            st.session_state.show_result = False
            play_sound("new_task")
            st.rerun()
        else:
            remaining = 2 - elapsed
            st.info(f"⏳ New task in {int(remaining)}s...")
    if st.session_state.get("current_task"):
        task = st.session_state.current_task
        if st.session_state.get("task_submitted", False):
            user_ans = st.session_state.get("user_answer", 0)
            correct_ans = task["correct_answer"]
            if user_ans == correct_ans:
                st.markdown(f'<div class="success-msg">🎉 Correct! +{st.session_state.last_points} points!</div>', unsafe_allow_html=True)
                play_sound("correct")
                save_leaderboard_entry(st.session_state.username, st.session_state.score)
            else:
                st.markdown(f'<div class="error-msg">❌ Incorrect<br>Correct answer: {correct_ans}</div>', unsafe_allow_html=True)
                play_sound("wrong")
            st.markdown(show_calculation_breakdown(task), unsafe_allow_html=True)
            st.markdown(show_share_buttons(st.session_state.score, st.session_state.streak), unsafe_allow_html=True)
            st.session_state.show_result = True
            st.session_state.result_time = time.time()
        if not st.session_state.get("task_submitted", False):
            st.markdown(f'<div class="task-display task-entrance" key="task_{st.session_state.get("task_key", 0)}">', unsafe_allow_html=True)
            st.markdown(f'<span class="exercise-icon">{task["icon"]}</span>', unsafe_allow_html=True)
            st.markdown(f'<h2 style="color: white; text-align: center; margin: 15px 0;">{task["exercise"]}</h2>', unsafe_allow_html=True)
            st.markdown('---', unsafe_allow_html=True)
            if task["type"] == "cash":
                st.markdown(f'<p style="font-size: 2rem; font-weight: bold; color: white;">🧾 Price: <span style="color: #00d4ff;">${task["price"]}</span><br>💰 Paid: <span style="color: #00d4ff;">${task["paid"]}</span></p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Change:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "billing":
                st.markdown(f'<p style="font-size: 1.8rem; font-weight: bold; color: white;">📋 {task["service"]}<br>📅 {task["total_days"]} days<br>❌ Missed: {task["missed_days"]}<br>💰 ₹{task["daily_cost"]}/day</p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Amount:", min_value=0, step=1, key="ans")
            elif task["type"] == "tip":
                st.markdown(f'<p style="font-size: 2rem; font-weight: bold; color: white;">💵 Bill: <span style="color: #00d4ff;">${task["bill"]}</span><br>💝 Tip: <span style="color: #f107a3;">{task["tip_percent"]}%</span></p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Tip:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "discount":
                st.markdown(f'<p style="font-size: 2rem; font-weight: bold; color: white;">💰 Price: <span style="color: #00d4ff;">${task["original_price"]}</span><br>📉 Discount: <span style="color: #f107a3;">{task["discount_percent"]}%</span></p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Final:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "tax":
                st.markdown(f'<p style="font-size: 2rem; font-weight: bold; color: white;">💵 Price: <span style="color: #00d4ff;">${task["price"]}</span><br>📊 Tax: <span style="color: #f107a3;">{task["tax_rate"]}%</span></p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Tax:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "split":
                st.markdown(f'<p style="font-size: 1.8rem; font-weight: bold; color: white;">💵 Total: <span style="color: #00d4ff;">${task["total"]}</span><br>👥 People: {task["people"]}<br>💝 Tip: {task["tip"]}%</p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Per person:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "profit":
                st.markdown(f'<p style="font-size: 2rem; font-weight: bold; color: white;">💰 Cost: <span style="color: #00d4ff;">${task["cost_price"]}</span><br>📈 Markup: <span style="color: #f107a3;">{task["markup_percent"]}%</span></p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Profit:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "unit":
                st.markdown(f'<p style="font-size: 1.5rem; font-weight: bold; color: white;">🛒 Option 1: ${task["price1"]} for {task["qty1"]} = ${task["unit1"]}/item<br>🛒 Option 2: ${task["price2"]} for {task["qty2"]} = ${task["unit2"]}/item</p>', unsafe_allow_html=True)
                user_input = st.selectbox("👍 Better option:", [1, 2], key="ans")
            elif task["type"] == "percent":
                st.markdown(f'<p style="font-size: 2rem; font-weight: bold; color: white;">🔢 What is <span style="color: #f107a3;">{task["percent"]}%</span> of <span style="color: #00d4ff;">{task["number"]}</span>?</p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Answer:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "currency":
                st.markdown(f'<p style="color: #00d4ff; font-size: 1rem;">💡 Rate: 1 {task["from_currency"]} = {task["rate"]} {task["to_currency"]}</p><p style="font-size: 1.8rem; font-weight: bold; color: white;">💱 Convert {task["from_currency"]} {task["amount"]} to {task["to_currency"]}</p>', unsafe_allow_html=True)
                user_input = st.number_input(f"💵 Result:", min_value=0.0, step=0.01, key="ans")
            elif task["type"] == "interest":
                st.markdown(f'<p style="font-size: 1.8rem; font-weight: bold; color: white;">💰 Principal: <span style="color: #00d4ff;">${task["principal"]}</span><br>📊 Rate: <span style="color: #f107a3;">{task["rate"]}%</span><br>📅 Years: <span style="color: #7b2ff7;">{task["years"]}</span></p>', unsafe_allow_html=True)
                user_input = st.number_input("💵 Interest:", min_value=0.0, step=0.01, key="ans")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                correct = task["correct_answer"]
                if user_input == correct:
                    time_taken = time.time() - st.session_state.start_time
                    base = 10 * DIFFICULTY_SETTINGS[difficulty]["points_multiplier"]
                    bonus = max(0, int((DIFFICULTY_SETTINGS[difficulty]["time_limit"] - time_taken) / 5))
                    total = base + bonus
                    st.session_state.score += total
                    st.session_state.streak += 1
                    st.session_state.last_points = total
                else:
                    st.session_state.streak = 0
                entry = {"Timestamp": datetime.now().isoformat(), "Mode": task["exercise"], "Exercise": task["exercise"], "Difficulty": difficulty, "UserAnswer": user_input, "CorrectAnswer": correct, "Status": "Correct" if user_input == correct else "Incorrect", "TimeTaken": round(time.time() - st.session_state.start_time, 2), "Points": st.session_state.last_points if user_input == correct else 0}
                save_user_progress(st.session_state.username, entry)
                st.session_state.user_answer = user_input
                st.session_state.task_submitted = True
                st.rerun()

def progress_page():
    custom_css()
    st.markdown('<h2 style="color: white; text-align: center; font-size: 2rem;">📊 Your Progress</h2>', unsafe_allow_html=True)
    progress = load_user_progress(st.session_state.username)
    if progress.empty:
        st.markdown('<div class="card"><p style="text-align: center; color: white; font-size: 1.2rem;">No exercises yet. Start practicing! 🎮</p></div>', unsafe_allow_html=True)
        return
    total = len(progress)
    correct = len(progress[progress["Status"] == "Correct"])
    accuracy = (correct / total * 100) if total > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    stats_data = [("📝", total, "Exercises", "#00d4ff"), ("✅", f"{accuracy:.0f}%", "Accuracy", "#00b09b"), ("🏆", int(progress["Points"].sum()), "Points", "#7b2ff7"), ("⏱️", f"{progress['TimeTaken'].mean():.1f}s", "Avg Time", "#f107a3")]
    for i, (icon, value, label, color) in enumerate(stats_data):
        with eval(f"col{i+1}"):
            st.markdown(f'''<div class="stat-card"><div style="font-size: 2rem;">{icon}</div><h2 style="color: {color};">{value}</h2><p>{label}</p></div>''', unsafe_allow_html=True)
    if len(progress) > 1:
        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["📈 Accuracy Trend", "⏱️ Time Analysis", "🎯 By Exercise"])
        with tab1:
            progress["StatusNum"] = (progress["Status"] == "Correct").astype(int)
            progress["Rolling"] = progress["StatusNum"].rolling(5).mean() * 100
            st.line_chart(progress["Rolling"].dropna(), use_container_width=True)
        with tab2:
            st.line_chart(progress["TimeTaken"], use_container_width=True)
        with tab3:
            stats = progress.groupby("Exercise").agg({"Status": lambda x: (x == "Correct").mean() * 100, "Points": "sum"}).round(1)
            stats.columns = ["Accuracy %", "Points"]
            st.dataframe(stats, use_container_width=True)
    st.markdown("---")
    st.markdown('<h3 style="color: white;">📝 Recent Activity</h3>', unsafe_allow_html=True)
    st.dataframe(progress.tail(10)[["Timestamp", "Exercise", "Difficulty", "Status", "Points"]], use_container_width=True)
    csv = progress.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Log", csv, f"{st.session_state.username}_progress.csv", "text/csv", use_container_width=True)

def settings_page():
    custom_css()
    st.markdown('<h2 style="color: white; text-align: center; font-size: 2rem;">⚙️ Settings</h2>', unsafe_allow_html=True)
    current_settings = st.session_state.get("settings", load_settings(st.session_state.username))
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sound = st.toggle("🔊 Sound Effects", value=current_settings.get("sound_enabled", True))
        diff = st.selectbox("📊 Default Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(current_settings.get("default_difficulty", "Medium")))
        ex = st.selectbox("🎯 Default Exercise", EXERCISE_NAMES, index=EXERCISE_NAMES.index(current_settings.get("default_exercise", "Cash Counting")))
        st.markdown("---")
        col1, col2 = st.columns(2)
        if col1.button("💾 Save Settings", use_container_width=True):
            save_settings(st.session_state.username, {"sound_enabled": sound, "default_difficulty": diff, "default_exercise": ex})
            st.session_state.settings = {"sound_enabled": sound, "default_difficulty": diff, "default_exercise": ex}
            st.success("✅ Settings saved!")
        if col2.button("🗑️ Reset Progress", use_container_width=True):
            reset_user_progress(st.session_state.username)
            st.session_state.score = 0
            st.session_state.streak = 0
            st.success("✅ Progress reset!")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== LEGAL PAGES ====================
def show_privacy_policy_page():
    custom_css()
    st.markdown('<p class="main-title">📜 Privacy Policy</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown("""
    **Last Updated:** January 2025

    ## Overview

    MathBlitz ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how your personal information is collected, used, and disclosed by MathBlitz.

    ## Information We Collect

    ### Information You Provide
    - **Account Information:** When you register, we collect your username and password.
    - **Progress Data:** We store your practice progress, scores, and achievements.
    - **Settings:** We save your preferences (sound settings, default difficulty, etc.)

    ### Automatically Collected Information
    - **Usage Data:** We collect information about how you use the app (exercises completed, time spent, etc.)
    - **Device Information:** Basic device information for app functionality

    ## How We Use Your Information

    We use your information to:
    - Provide and improve our math practice services
    - Track your progress and achievements
    - Maintain leaderboard rankings
    - Save your preferences and settings
    - Communicate important updates

    ## Data Storage

    - All user data is stored locally on your device
    - Progress data is saved as CSV files in your local `data/progress` folder
    - User credentials are stored in `data/users.json`
    - We do not sell or share your personal information with third parties

    ## Data Security

    We implement appropriate security measures to protect your personal information:
    - Passwords are stored securely
    - Local data storage is protected by your device's security
    - No sensitive payment information is collected

    ## Your Rights

    You have the right to:
    - Access your personal data
    - Delete your account and associated data
    - Reset your progress at any time
    - Export your data in CSV format

    ## Children's Privacy

    MathBlitz is designed for general audiences, including children. We do not knowingly collect personal information from children under 13 without parental consent.

    ## Changes to This Policy

    We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page.

    ## Contact Us

    If you have any questions about this Privacy Policy, please contact us through the app.

    ---

    By using MathBlitz, you agree to the terms outlined in this Privacy Policy.
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 Back to Login", use_container_width=True):
        st.session_state.show_privacy_policy = False
        st.rerun()

def show_terms_of_service_page():
    custom_css()
    st.markdown('<p class="main-title">📋 Terms of Service</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown("""
    **Last Updated:** January 2025

    ## Acceptance of Terms

    By accessing and using MathBlitz ("the App"), you accept and agree to be bound by the terms and provision of this agreement.

    ## Description of Service

    MathBlitz is an interactive math practice application that provides:
    - 11 different math exercise types
    - Gamification features including scoring and streaks
    - World leaderboard rankings
    - User progress tracking
    - Multiple difficulty levels

    ## User Accounts

    ### Registration
    - You must provide accurate and complete registration information
    - You are responsible for maintaining the security of your account
    - You must be at least 13 years old to create an account

    ### Account Responsibilities
    - You are solely responsible for all activities under your account
    - You must notify us immediately of any unauthorized use
    - You agree not to share your account credentials with others

    ## Acceptable Use

    You agree not to:
    - Use the app for any unlawful purpose
    - Attempt to gain unauthorized access to any part of the app
    - Interfere with the proper operation of the app
    - Submit false or misleading information
    - Create multiple accounts to manipulate leaderboards

    ## Intellectual Property

    - All content and materials in MathBlitz are owned by us
    - You may not copy, modify, or distribute our content without permission
    - The "MathBlitz" name and logo are our trademarks

    ## User-Generated Content

    You retain ownership of any progress data you generate while using the app. By using the app, you grant us the right to display your username and scores on the leaderboard.

    ## Disclaimers

    THE APP IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. WE DO NOT GUARANTEE THAT THE APP WILL BE UNINTERRUPTED OR ERROR-FREE.

    ## Limitation of Liability

    We shall not be liable for any indirect, incidental, or consequential damages arising from your use of the app.

    ## Termination

    We reserve the right to terminate or suspend your account at any time for violation of these terms.

    ## Changes to Terms

    We may modify these terms at any time. Continued use of the app constitutes acceptance of updated terms.

    ## Governing Law

    These terms shall be governed by and construed in accordance with applicable laws.

    ## Contact

    For questions about these Terms of Service, please contact us through the app.

    ---

    By using MathBlitz, you acknowledge that you have read and understood these Terms of Service and agree to be bound by them.
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 Back to Login", use_container_width=True):
        st.session_state.show_terms_of_service = False
        st.rerun()

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Try to restore session from localStorage (only on first load)
    if not st.session_state.logged_in and "session_restored" not in st.session_state:
        # Use Streamlit's on_change callback mechanism via JavaScript
        st.markdown("""
        <script>
        // Check for saved session on page load
        (function() {
            try {
                var stored = localStorage.getItem('mathblitz_user');
                if (stored) {
                    var data = JSON.parse(stored);
                    var sevenDays = 7 * 24 * 60 * 60 * 1000;
                    if (new Date().getTime() - data.timestamp < sevenDays) {
                        // Store username to restore after page reload
                        sessionStorage.setItem('restore_user', data.username);
                    }
                }
            } catch(e) {}
        })();
        </script>
        """, unsafe_allow_html=True)
        
        # Check if we should restore session (via query params workaround)
        # Since Streamlit doesn't support direct session restoration from JS,
        # we'll rely on the login form to persist session
        st.session_state.session_restored = True
    
    if not st.session_state.logged_in:
        login_page()
        return
    page = sidebar()
    st.session_state.settings = load_settings(st.session_state.username)
    if page == "practice" or page == "🎮":
        exercise_page()
    elif page == "progress" or page == "📊":
        progress_page()
    elif page == "settings" or page == "⚙️":
        settings_page()

if __name__ == "__main__":
    main()
