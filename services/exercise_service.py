"""Exercise generation service for MathBlitz"""
import random
from typing import Dict, Any, List

from config.settings import (
    FORMULAS,
    SERVICES,
    CURRENCY_RATES,
    DIFFICULTY_SETTINGS,
    EXERCISE_NAMES
)


class ExerciseService:
    """Handles exercise generation logic"""
    
    def __init__(self):
        self.formulas = FORMULAS
        self.services = SERVICES
        self.currency_rates = CURRENCY_RATES
        self.difficulty_settings = DIFFICULTY_SETTINGS
        self.exercise_names = EXERCISE_NAMES
    
    def get_formula(self, exercise_name: str) -> Dict[str, str]:
        """Get formula details for an exercise"""
        return self.formulas.get(exercise_name, {})
    
    def get_all_formulas(self) -> Dict[str, Dict[str, str]]:
        """Get all exercise formulas"""
        return self.formulas
    
    def get_time_limit(self, difficulty: str) -> int:
        """Get time limit for a difficulty"""
        return self.difficulty_settings.get(difficulty, {}).get("time_limit", 45)
    
    def get_points_multiplier(self, difficulty: str) -> int:
        """Get points multiplier for a difficulty"""
        return self.difficulty_settings.get(difficulty, {}).get("points_multiplier", 1)
    
    def calculate_points(self, difficulty: str, time_taken: float) -> int:
        """Calculate points for a correct answer"""
        base = 10 * self.get_points_multiplier(difficulty)
        time_limit = self.get_time_limit(difficulty)
        bonus = max(0, int((time_limit - time_taken) / 5))
        return base + bonus
    
    def generate_task(self, exercise: str, difficulty: str) -> Dict[str, Any]:
        """
        Generate a math task
        
        Args:
            exercise: The exercise name
            difficulty: The difficulty level
            
        Returns:
            Dictionary containing task details
        """
        # Default to Cash Counting if exercise not found
        if exercise not in self.exercise_names:
            exercise = "Cash Counting"
        
        # Generate task based on exercise type
        generators = {
            "Cash Counting": self._generate_cash_counting,
            "Billing Calculation": self._generate_billing,
            "Tip Calculator": self._generate_tip,
            "Discount Calculator": self._generate_discount,
            "Tax Calculator": self._generate_tax,
            "Split Bill": self._generate_split,
            "Profit/Loss": self._generate_profit,
            "Unit Price Compare": self._generate_unit_price,
            "Percentage": self._generate_percentage,
            "Currency Convert": self._generate_currency,
            "Simple Interest": self._generate_interest,
            "Compound Interest": self._generate_compound_interest,
            "Multiplication": self._generate_multiplication
        }
        
        generator = generators.get(exercise, self._generate_cash_counting)
        return generator(difficulty)
    
    def _generate_cash_counting(self, difficulty: str) -> Dict[str, Any]:
        """Generate Cash Counting task"""
        max_price = 50 if difficulty == "Easy" else 200 if difficulty == "Medium" else 500
        max_paid = 20 if difficulty == "Easy" else 50 if difficulty == "Medium" else 100
        
        price = random.randint(1, max_price)
        paid = price + random.randint(1, max_paid)
        
        return {
            "exercise": "Cash Counting",
            "icon": "🎮",
            "type": "cash",
            "price": price,
            "paid": paid,
            "correct_answer": paid - price
        }
    
    def _generate_billing(self, difficulty: str) -> Dict[str, Any]:
        """Generate Billing Calculation task"""
        service = random.choice(list(self.services.keys()))
        daily = self.services[service]
        
        total_days = random.randint(10, 20) if difficulty == "Easy" else random.randint(20, 31) if difficulty == "Medium" else random.randint(25, 60)
        missed = random.randint(0, 2) if difficulty == "Easy" else random.randint(0, 4) if difficulty == "Medium" else random.randint(1, 8)
        
        return {
            "exercise": "Billing Calculation",
            "icon": "🧾",
            "type": "billing",
            "service": service,
            "total_days": total_days,
            "missed_days": missed,
            "daily_cost": daily,
            "correct_answer": (total_days - missed) * daily
        }
    
    def _generate_tip(self, difficulty: str) -> Dict[str, Any]:
        """Generate Tip Calculator task"""
        min_bill = 20 if difficulty == "Easy" else 50 if difficulty == "Medium" else 100
        max_bill = 100 if difficulty == "Easy" else 300 if difficulty == "Medium" else 1000
        
        bill = random.randint(min_bill, max_bill)
        tip = random.choice([10, 15, 18, 20, 25])
        
        return {
            "exercise": "Tip Calculator",
            "icon": "🍽️",
            "type": "tip",
            "bill": bill,
            "tip_percent": tip,
            "correct_answer": round(bill * tip / 100, 2)
        }
    
    def _generate_discount(self, difficulty: str) -> Dict[str, Any]:
        """Generate Discount Calculator task"""
        min_price = 50 if difficulty == "Easy" else 100 if difficulty == "Medium" else 200
        max_price = 200 if difficulty == "Easy" else 500 if difficulty == "Medium" else 2000
        
        price = random.randint(min_price, max_price)
        disc = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
        
        return {
            "exercise": "Discount Calculator",
            "icon": "🏷️",
            "type": "discount",
            "original_price": price,
            "discount_percent": disc,
            "correct_answer": round(price * (100 - disc) / 100, 2)
        }
    
    def _generate_tax(self, difficulty: str) -> Dict[str, Any]:
        """Generate Tax Calculator task"""
        min_price = 50 if difficulty == "Easy" else 100 if difficulty == "Medium" else 200
        max_price = 200 if difficulty == "Easy" else 500 if difficulty == "Medium" else 2000
        
        price = random.randint(min_price, max_price)
        tax = random.choice([5, 7, 8, 10, 12, 15])
        
        return {
            "exercise": "Tax Calculator",
            "icon": "🧾",
            "type": "tax",
            "price": price,
            "tax_rate": tax,
            "correct_answer": round(price * tax / 100, 2)
        }
    
    def _generate_split(self, difficulty: str) -> Dict[str, Any]:
        """Generate Split Bill task"""
        min_total = 30 if difficulty == "Easy" else 50 if difficulty == "Medium" else 100
        max_total = 150 if difficulty == "Easy" else 300 if difficulty == "Medium" else 1000
        
        total = random.randint(min_total, max_total)
        people = random.randint(2, 4) if difficulty == "Easy" else random.randint(2, 6) if difficulty == "Medium" else random.randint(2, 10)
        tip = random.choice([0, 10, 15, 20])
        
        return {
            "exercise": "Split Bill",
            "icon": "👥",
            "type": "split",
            "total": total,
            "people": people,
            "tip": tip,
            "correct_answer": round(total * (100 + tip) / 100 / people, 2)
        }
    
    def _generate_profit(self, difficulty: str) -> Dict[str, Any]:
        """Generate Profit/Loss task"""
        min_cost = 20 if difficulty == "Easy" else 50 if difficulty == "Medium" else 100
        max_cost = 100 if difficulty == "Easy" else 300 if difficulty == "Medium" else 1000
        
        cost = random.randint(min_cost, max_cost)
        markup = random.randint(10, 50)
        
        return {
            "exercise": "Profit/Loss",
            "icon": "📈",
            "type": "profit",
            "cost_price": cost,
            "markup_percent": markup,
            "correct_answer": round(cost * markup, 2)
        }
    
    def _generate_unit_price(self, difficulty: str) -> Dict[str, Any]:
        """Generate Unit Price Compare task"""
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
        
        return {
            "exercise": "Unit Price Compare",
            "icon": "⚖️",
            "type": "unit",
            "price1": p1,
            "qty1": q1,
            "price2": p2,
            "qty2": q2,
            "correct_answer": 1 if u1 < u2 else 2,
            "unit1": round(u1, 2),
            "unit2": round(u2, 2)
        }
    
    def _generate_percentage(self, difficulty: str) -> Dict[str, Any]:
        """Generate Percentage task"""
        if difficulty == "Easy":
            num = random.randint(10, 100)
            pct = random.choice([10, 20, 25, 50, 75])
        elif difficulty == "Medium":
            num = random.randint(50, 500)
            pct = random.randint(5, 50)
        else:
            num = random.randint(100, 1000)
            pct = random.randint(1, 75)
        
        return {
            "exercise": "Percentage",
            "icon": "🔢",
            "type": "percent",
            "number": num,
            "percent": pct,
            "correct_answer": round(num * pct / 100, 2)
        }
    
    def _generate_currency(self, difficulty: str) -> Dict[str, Any]:
        """Generate Currency Convert task"""
        currencies = list(self.currency_rates.keys())
        base_currency = random.choice(currencies)
        rates = self.currency_rates[base_currency]
        target = random.choice(list(rates.keys()))
        
        min_amount = 10 if difficulty == "Easy" else 50 if difficulty == "Medium" else 100
        max_amount = 100 if difficulty == "Easy" else 500 if difficulty == "Medium" else 2000
        
        amount = random.randint(min_amount, max_amount)
        rate = rates[target]
        
        return {
            "exercise": "Currency Convert",
            "icon": "💱",
            "type": "currency",
            "from_currency": base_currency,
            "to_currency": target,
            "amount": amount,
            "rate": rate,
            "correct_answer": round(amount * rate, 2)
        }
    
    def _generate_interest(self, difficulty: str) -> Dict[str, Any]:
        """Generate Simple Interest task"""
        min_principal = 100 if difficulty == "Easy" else 500 if difficulty == "Medium" else 1000
        max_principal = 1000 if difficulty == "Easy" else 5000 if difficulty == "Medium" else 20000
        
        principal = random.randint(min_principal, max_principal)
        rate = random.randint(5, 15)
        
        if difficulty == "Easy":
            years = random.randint(1, 3)
        elif difficulty == "Medium":
            years = random.randint(1, 5)
        else:
            years = random.randint(1, 10)
        
        return {
            "exercise": "Simple Interest",
            "icon": "📊",
            "type": "interest",
            "principal": principal,
            "rate": rate,
            "years": years,
            "correct_answer": round(principal * rate * years / 100, 2)
        }
    
    def _generate_compound_interest(self, difficulty: str) -> Dict[str, Any]:
        """Generate Compound Interest task - calculates final amount"""
        # Principal amounts based on difficulty
        min_principal = 500 if difficulty == "Easy" else 1000 if difficulty == "Medium" else 2000
        max_principal = 2000 if difficulty == "Easy" else 10000 if difficulty == "Medium" else 50000
        
        principal = random.randint(min_principal, max_principal)
        
        # Interest rates based on difficulty
        if difficulty == "Easy":
            rate = random.choice([5, 8, 10, 12])
            years = random.randint(1, 3)
        elif difficulty == "Medium":
            rate = random.choice([8, 10, 12, 15])
            years = random.randint(2, 5)
        else:
            rate = random.choice([10, 12, 15, 18, 20])
            years = random.randint(2, 10)
        
        # Compound interest formula: A = P(1 + r/n)^(nt)
        # Assuming annual compounding (n=1) for simplicity
        # A = P(1 + r/100)^t
        amount = principal * ((1 + rate / 100) ** years)
        
        return {
            "exercise": "Compound Interest",
            "icon": "💹",
            "type": "compound_interest",
            "principal": principal,
            "rate": rate,
            "years": years,
            "correct_answer": round(amount, 2)
        }
    
    def _generate_multiplication(self, difficulty: str) -> Dict[str, Any]:
        """Generate Multiplication task (tables 2-20)"""
        # Easy: tables 2-5, Medium: tables 2-10, Hard: tables 2-20
        if difficulty == "Easy":
            min_table, max_table = 2, 5
            max_factor = 10
        elif difficulty == "Medium":
            min_table, max_table = 2, 10
            max_factor = 12
        else:
            min_table, max_table = 2, 20
            max_factor = 15
        
        # Generate two numbers to multiply
        table = random.randint(min_table, max_table)
        factor = random.randint(1, max_factor)
        
        return {
            "exercise": "Multiplication",
            "icon": "✖️",
            "type": "multiplication",
            "number1": table,
            "number2": factor,
            "correct_answer": table * factor
        }
    
    def get_share_text(self, score: int, streak: int) -> str:
        """Generate share text for social media"""
        return f"🎉 I just scored {score} points with a {streak} streak on MathBlitz! 💵🧮 Play now: https://mathblitz.streamlit.app #MathBlitz #MathSkills"


# Create singleton instance
exercise_service = ExerciseService()

