import streamlit as st
import random
import pandas as pd
from datetime import datetime

# Initialize session state for logs and task
def init_state():
    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "task" not in st.session_state:
        st.session_state.task = None

init_state()

# Define services to simulate real-life billing
SERVICES = {
    "Milk Delivery": {"cost_per_day": 30},
    "Newspaper": {"cost_per_day": 5},
    "Water Can Delivery": {"cost_per_day": 20},
    "Laundry Pickup": {"cost_per_day": 50}
}

# Generate a new billing task
def generate_task():
    service = random.choice(list(SERVICES.keys()))
    total_days = random.randint(20, 31)
    missed_days = random.randint(0, 5)
    actual_days = total_days - missed_days
    daily_cost = SERVICES[service]["cost_per_day"]
    claimed_amount = total_days * daily_cost
    correct_amount = actual_days * daily_cost

    st.session_state.task = {
        "service": service,
        "total_days": total_days,
        "missed_days": missed_days,
        "claimed_amount": claimed_amount,
        "correct_amount": correct_amount,
        "daily_cost": daily_cost,
        "actual_days": actual_days,
    }

# Log the result
def log_result(user_input, status):
    log = {
        "timestamp": datetime.now(),
        "service": st.session_state.task["service"],
        "claimed": st.session_state.task["claimed_amount"],
        "your_input": user_input,
        "correct": st.session_state.task["correct_amount"],
        "status": status
    }
    st.session_state.logs.append(log)

st.title("🧾 Real-Life Billing Calculator Simulator")

if st.button("🔄 Generate New Task"):
    generate_task()

if st.session_state.task:
    task = st.session_state.task
    st.subheader(f"Service: {task['service']}")
    st.write(f"Vendor claimed ₹{task['claimed_amount']} for {task['total_days']} days.")
    st.write(f"You know {task['missed_days']} days were missed. Daily cost is ₹{task['daily_cost']}")

    user_input = st.number_input("Enter the correct amount to be paid:", min_value=0, step=1)

    if st.button("✅ Submit"):
        if user_input == task["correct_amount"]:
            st.success("✅ Correct! You calculated it perfectly.")
            log_result(user_input, "Correct")
        else:
            st.error(f"❌ Incorrect. The correct amount was ₹{task['correct_amount']}.")
            log_result(user_input, "Incorrect")

# Display logs and download option
if st.session_state.logs:
    df = pd.DataFrame(st.session_state.logs)
    st.write("### 📊 Your Task History")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV Log", csv, "billing_log.csv", "text/csv")
