import streamlit as st
import random
import time
import pandas as pd
import pygame
from datetime import datetime
import os

# Initialize sound system
pygame.mixer.init()

def play_sound(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except Exception as e:
        st.warning(f"Sound error: {e}")

# Initialize log file
LOG_FILE = "log.csv"
if "log_initialized" not in st.session_state:
    if not pd.io.common.file_exists(LOG_FILE):
        pd.DataFrame(columns=["Task", "UserAnswer", "CorrectAnswer", "Status", "TimeTaken"]).to_csv(LOG_FILE, index=False)
    st.session_state.log_initialized = True

# Create a new task with 2 to 4 digit prices and paid amounts
def create_task():
    price = random.randint(1, 100)
    #paid = price + random.choice([0,1, 5, 10, 20, 50, 100])
    paid = price + random.randint(1, 100)
    #return round(price, 2), round(paid, 2)
    return price, paid

# Initialize session state
if "price" not in st.session_state:
    st.session_state.price, st.session_state.paid = create_task()
    play_sound("sounds/new_task.wav")
    st.session_state.start_time = time.time()
    st.session_state.task_submitted = False
    st.session_state.result_message = ""

# Reset Streamlit widgets on each new task
def reset_task():
    st.session_state.price, st.session_state.paid = create_task()
    st.session_state.start_time = time.time()
    st.session_state.task_submitted = False
    st.session_state.result_message = ""
    st.rerun()  # Clear output and rerun app

st.title("💵 Cash Counting Practice")

st.write(f"🧾 **Item Price:** ${st.session_state.price}")
st.write(f"💰 **Customer Paid:** ${st.session_state.paid}")

user_change = st.number_input("Enter change to give:")

if st.button("✅ Submit"):
    end_time = time.time()
    time_taken = round(end_time - st.session_state.start_time, 2)
    correct_change = round(st.session_state.paid - st.session_state.price, 2)
    status = "Correct" if user_change == correct_change else "Incorrect"

    if status == "Correct":
        st.success(f"✅ Correct! Change: ${correct_change}")
        play_sound("sounds/correct.wav")
    else:
        st.error(f"❌ Incorrect. Correct change is ${correct_change}")
        play_sound("sounds/wrong.wav")

    result = {
        "Task": f"${st.session_state.paid} - ${st.session_state.price}",
        "UserAnswer": user_change,
        "CorrectAnswer": correct_change,
        "Status": status,
        "TimeTaken": time_taken,
    }
    df = pd.DataFrame([result])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

    st.session_state.task_submitted = True
    st.session_state.result_message = f"{status}! Time: {time_taken}s"

if st.session_state.task_submitted:
    st.write(f"📝 {st.session_state.result_message}")
    if st.button("➡️ Next Task"):
        reset_task()

# Show past performance
if st.checkbox("📊 Show Summary Graph"):
    try:
        data = pd.read_csv(LOG_FILE)
        st.line_chart(data["TimeTaken"])
        st.write(data.tail())
        st.download_button("⬇️ Download CSV", data.to_csv(index=False), file_name="log.csv")
    except Exception as e:
        st.warning(f"Error loading log: {e}")
