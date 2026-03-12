"""Modal components for MathBlitz - Modern Clean Design"""
import streamlit as st
from typing import Dict, Any


def render_calculation_breakdown(task: Dict[str, Any]) -> None:
    """
    Render the calculation breakdown for a task
    
    Args:
        task: The task dictionary with all details
    """
    calc_html = '<div class="calc-breakdown"><div class="calc-title">📝 Calculation Breakdown</div>'
    
    task_type = task.get("type", "")
    
    if task_type == "cash":
        calc_html += f'''<div class="calc-step">Step 1: Price = ${task["price"]}</div>
        <div class="calc-step">Step 2: Paid = ${task["paid"]}</div>
        <div class="calc-step">Step 3: Change = ${task["paid"]} - ${task["price"]}</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "billing":
        calc_html += f'''<div class="calc-step">Step 1: Total days claimed = {task["total_days"]}</div>
        <div class="calc-step">Step 2: Missed days = {task["missed_days"]}</div>
        <div class="calc-step">Step 3: Actual days = {task["total_days"]} - {task["missed_days"]} = {task["total_days"] - task["missed_days"]}</div>
        <div class="calc-step">Step 4: Amount = {task["total_days"] - task["missed_days"]} × ${task["daily_cost"]}</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "tip":
        calc_html += f'''<div class="calc-step">Step 1: Bill = ${task["bill"]}</div>
        <div class="calc-step">Step 2: Tip = {task["tip_percent"]}%</div>
        <div class="calc-step">Step 3: Tip = ${task["bill"]} × {task["tip_percent"]/100}</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "discount":
        calc_html += f'''<div class="calc-step">Step 1: Original = ${task["original_price"]}</div>
        <div class="calc-step">Step 2: Discount = {task["discount_percent"]}%</div>
        <div class="calc-step">Step 3: Final = ${task["original_price"]} × {100-task["discount_percent"]}/100</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "tax":
        calc_html += f'''<div class="calc-step">Step 1: Price = ${task["price"]}</div>
        <div class="calc-step">Step 2: Tax = {task["tax_rate"]}%</div>
        <div class="calc-step">Step 3: Tax = ${task["price"]} × {task["tax_rate"]/100}</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "split":
        calc_html += f'''<div class="calc-step">Step 1: Total = ${task["total"]}</div>
        <div class="calc-step">Step 2: Tip = {task["tip"]}%</div>
        <div class="calc-step">Step 3: People = {task["people"]}</div>
        <div class="calc-step">Step 4: Per person = ${task["total"]} × (100+{task["tip"]})/100 ÷ {task["people"]}</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "profit":
        calc_html += f'''<div class="calc-step">Step 1: Cost = ${task["cost_price"]}</div>
        <div class="calc-step">Step 2: Markup = {task["markup_percent"]}%</div>
        <div class="calc-step">Step 3: Profit = ${task["cost_price"]} × {task["markup_percent"]/100}</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "unit":
        calc_html += f'''<div class="calc-step">Option 1: ${task["price1"]} ÷ {task["qty1"]} = ${task["unit1"]}/item</div>
        <div class="calc-step">Option 2: ${task["price2"]} ÷ {task["qty2"]} = ${task["unit2"]}/item</div>
        <div class="calc-result">✓ Better option: {task["correct_answer"]}</div>'''
    
    elif task_type == "percent":
        calc_html += f'''<div class="calc-step">Step 1: Number = {task["number"]}</div>
        <div class="calc-step">Step 2: {task["percent"]}% of {task["number"]}</div>
        <div class="calc-step">Step 3: {task["number"]} × {task["percent"]/100}</div>
        <div class="calc-result">✓ Answer: {task["correct_answer"]}</div>'''
    
    elif task_type == "currency":
        calc_html += f'''<div class="calc-step">Step 1: {task["amount"]} {task["from_currency"]}</div>
        <div class="calc-step">Step 2: Rate = {task["rate"]}</div>
        <div class="calc-step">Step 3: {task["amount"]} × {task["rate"]}</div>
        <div class="calc-result">✓ Answer: {task["correct_answer"]} {task["to_currency"]}</div>'''
    
    elif task_type == "interest":
        calc_html += f'''<div class="calc-step">Step 1: Principal = ${task["principal"]}</div>
        <div class="calc-step">Step 2: Rate = {task["rate"]}%</div>
        <div class="calc-step">Step 3: Years = {task["years"]}</div>
        <div class="calc-step">Step 4: ${task["principal"]} × {task["rate"]} × {task["years"]} ÷ 100</div>
        <div class="calc-result">✓ Answer: ${task["correct_answer"]}</div>'''
    
    elif task_type == "multiplication":
        calc_html += f'''<div class="calc-step">Step 1: Number 1 = {task["number1"]}</div>
        <div class="calc-step">Step 2: Number 2 = {task["number2"]}</div>
        <div class="calc-step">Step 3: Multiply = {task["number1"]} × {task["number2"]}</div>
        <div class="calc-result">✓ Answer: {task["correct_answer"]}</div>'''
    
    calc_html += '</div>'
    st.markdown(calc_html, unsafe_allow_html=True)


def render_share_buttons(score: int, streak: int) -> None:
    """
    Render social media share buttons
    
    Args:
        score: Current score
        streak: Current streak
    """
    from services import exercise_service
    
    share_text = exercise_service.get_share_text(score, streak)
    encoded_text = share_text.replace(" ", "%20").replace("!", "%21").replace("#", "%23")
    
    html = '<div class="share-container">'
    html += f'<a href="https://twitter.com/intent/tweet?text={encoded_text}" target="_blank" class="share-btn share-x">𝕏 Post</a>'
    html += f'<a href="https://www.facebook.com/sharer/sharer.php?u=https://mathblitz.streamlit.app&quote={encoded_text}" target="_blank" class="share-btn share-fb">f Facebook</a>'
    html += f'<a href="https://wa.me/?text={encoded_text}" target="_blank" class="share-btn share-whatsapp">📱 WhatsApp</a>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)


def render_timer_display(time_remaining: float, difficulty: str = "Medium") -> None:
    """
    Render a timer display with color based on time remaining
    
    Args:
        time_remaining: Seconds remaining
        difficulty: Current difficulty (for styling reference)
    """
    if time_remaining > 20:
        timer_class = "timer-easy"
    elif time_remaining > 10:
        timer_class = "timer-medium"
    else:
        timer_class = "timer-hard"
    
    st.markdown(
        f'<div class="timer-display {timer_class}">⏱️ {int(time_remaining)}s</div>',
        unsafe_allow_html=True
    )

