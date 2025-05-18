import streamlit as st
from db_connection import get_connection  # ✅ الاتصال الموحد

def login2():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            # ✅ إنشاء حساب المطور تلقائيًا لو مش موجود
            cursor.execute("SELECT * FROM users WHERE username = 'marwan_zynox_master'")
            if cursor.fetchone() is None:
                cursor.execute("""
                    INSERT INTO users (username, password, role)
                    VALUES (%s, %s, %s)
                """, ('marwan_zynox_master', 'marwanmaster99@', 'developer'))
                connection.commit()

            # ✅ التحقق من بيانات الدخول
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                st.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.user_role = user["role"]
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
        except Exception as e:
            st.error(f"Database error: {e}")
