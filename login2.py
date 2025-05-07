import streamlit as st
import mysql.connector

def login2():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MARWan99@",
                database="company_system"
            )
            cursor = connection.cursor(buffered=True)  # ✅ استخدم buffered هنا
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            cursor.close()  # ✅ مهم جدًا
            connection.close()

            if result:
                st.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        except Exception as e:
            st.error(f"Database error: {e}")
