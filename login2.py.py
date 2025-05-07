import streamlit as st
import mysql.connector

def login2():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MARWan99@",  # ← غيّرها لو مختلفه عندك
                database="company_system"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username=%s AND password=%s", (username, password))
            (count,) = cursor.fetchone()
            conn.close()

            if count == 1:
                st.session_state["logged_in"] = True
                st.success("✅ Login successful!")
            else:
                st.error("❌ Invalid username or password.")
        except Exception as e:
            st.error(f"Database error: {e}")
