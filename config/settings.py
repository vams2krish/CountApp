"""Application settings and configuration for MathBlitz"""
from pathlib import Path

# ==================== PATH CONFIG ====================
APP_DIR = Path(__file__).parent.parent
DATA_DIR = APP_DIR / "data"
SOUNDS_DIR = APP_DIR / "Sounds"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "progress").mkdir(exist_ok=True)

# ==================== FILE PATHS ====================
USERS_FILE = DATA_DIR / "users.json"
LEADERBOARD_FILE = DATA_DIR / "leaderboard.json"

# ==================== DIFFICULTY SETTINGS ====================
DIFFICULTY_SETTINGS = {
    "Easy": {"time_limit": 60, "points_multiplier": 1},
    "Medium": {"time_limit": 45, "points_multiplier": 2},
    "Hard": {"time_limit": 30, "points_multiplier": 3}
}

# ==================== EXERCISES CONFIG ====================
EXERCISES = [
    ("Cash Counting", "💵"),
    ("Billing Calculation", "🧾"),
    ("Tip Calculator", "🍽️"),
    ("Discount Calculator", "🏷️"),
    ("Tax Calculator", "📊"),
    ("Split Bill", "👥"),
    ("Profit/Loss", "📈"),
    ("Unit Price Compare", "⚖️"),
    ("Percentage", "🔢"),
    ("Currency Convert", "💱"),
    ("Simple Interest", "💰"),
    ("Compound Interest", "📈"),
    ("Multiplication", "✖️")
]

EXERCISE_NAMES = [e[0] for e in EXERCISES]

# ==================== EXERCISE FORMULAS ====================
FORMULAS = {
    "Cash Counting": {
        "icon": "🎮",
        "formula": "Change = Paid - Price",
        "example": "Price: $45, Paid: $50 → Change = $50 - $45 = $5",
        "tip": "Subtract the price from the amount paid"
    },
    "Billing Calculation": {
        "icon": "🧾",
        "formula": "Amount = (Total Days - Missed Days) × Daily Cost",
        "example": "30 days claimed, 5 missed, $20/day → (30-5) × $20 = $500",
        "tip": "First subtract missed days, then multiply by daily rate"
    },
    "Tip Calculator": {
        "icon": "🍽️",
        "formula": "Tip = Bill × (Tip% ÷ 100)",
        "example": "$100 bill, 15% tip → $100 × 0.15 = $15",
        "tip": "Move decimal 1 place left for 10%, double for 20%"
    },
    "Discount Calculator": {
        "icon": "🏷️",
        "formula": "Final = Original × (100 - Discount%) ÷ 100",
        "example": "$80 item, 25% off → $80 × 0.75 = $60",
        "tip": "Calculate discount amount first, subtract from original"
    },
    "Tax Calculator": {
        "icon": "🧾",
        "formula": "Tax = Price × (Tax% ÷ 100)",
        "example": "$50 item, 8% tax → $50 × 0.08 = $4",
        "tip": "Multiply price by tax rate as decimal"
    },
    "Split Bill": {
        "icon": "👥",
        "formula": "Per Person = (Total + Tip) ÷ People",
        "example": "$100 bill, 20% tip, 4 people → ($100 × 1.20) ÷ 4 = $30",
        "tip": "Add tip to total first, then divide by number of people"
    },
    "Profit/Loss": {
        "icon": "📈",
        "formula": "Profit = Cost × Markup%",
        "example": "$80 cost, 25% markup → $80 × 0.25 = $20 profit",
        "tip": "Profit = Selling Price - Cost Price"
    },
    "Unit Price Compare": {
        "icon": "⚖️",
        "formula": "Unit Price = Price ÷ Quantity",
        "example": "$10 for 5 items = $2/item",
        "tip": "Calculate price per item for each option, lower is better"
    },
    "Percentage": {
        "icon": "🔢",
        "formula": "Result = Number × (Percentage ÷ 100)",
        "example": "20% of 150 → 150 × 0.20 = 30",
        "tip": "Multiply number by percentage as decimal"
    },
    "Currency Convert": {
        "icon": "💱",
        "formula": "Result = Amount × Exchange Rate",
        "example": "$100 to EUR (0.85 rate) = $85 EUR",
        "tip": "Multiply amount by the conversion rate"
    },
    "Simple Interest": {
        "icon": "📊",
        "formula": "Interest = Principal × Rate × Time ÷ 100",
        "example": "$1000 at 5% for 2 years = $100 interest",
        "tip": "Principal × Rate × Years, then divide by 100"
    },
    "Compound Interest": {
        "icon": "💹",
        "formula": "A = P(1 + r/n)^(nt)",
        "example": "$1000 at 10% compounded annually for 2 years = $1210",
        "tip": "Amount = Principal × (1 + Rate/100)^Years"
    },
    "Multiplication": {
        "icon": "✖️",
        "formula": "Product = Number1 × Number2",
        "example": "7 × 8 = 56",
        "tip": "Multiply the two numbers together"
    }
}

# ==================== SERVICES DATA ====================
SERVICES = {
    "Milk Delivery": 30,
    "Newspaper": 5,
    "Water Can": 20,
    "Laundry": 50,
    "Gardening": 40,
    "Internet": 35
}

# ==================== CURRENCY RATES ====================
CURRENCY_RATES = {
    "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110, "INR": 74, "CAD": 1.25},
    "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 130, "INR": 87, "CAD": 1.47},
    "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150, "INR": 101, "CAD": 1.71},
    "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0099, "JPY": 1.5, "CAD": 0.017}
}

# ==================== DEFAULT SETTINGS ====================
DEFAULT_SETTINGS = {
    "sound_enabled": True,
    "default_difficulty": "Medium",
    "default_exercise": "Cash Counting"
}

# ==================== PAGE CONFIG ====================
PAGE_CONFIG = {
    "page_title": "MathBlitz",
    "page_icon": "🎮",
    "layout": "wide",
    "menu_items": {"About": "MathBlitz - Master math skills!"}
}

