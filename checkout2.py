import streamlit as st
import mysql.connector
from datetime import datetime

def checkout2():
    st.title("🔴 Check-Out")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MARWan99@",
        database="company_system"
    )
    cursor = connection.cursor()

    # جلب كل الموظفين
    cursor.execute("SELECT id, first_name, last_name, job_title FROM employees")
    employees = cursor.fetchall()

    employee_dict = {
        f"{emp[1]} {emp[2]} - {emp[3]}": emp[0]
        for emp in employees
    }

    selected = st.selectbox("🔍 Search and select your name:", list(employee_dict.keys()))

    if selected:
        employee_id = employee_dict[selected]

        if st.button("🚪 Check Out"):
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                UPDATE attendance
                SET check_out = %s
                WHERE employee_id = %s AND check_out IS NULL
                ORDER BY check_in DESC
                LIMIT 1
            """, (current_time, employee_id))
            connection.commit()

            if cursor.rowcount > 0:
                st.success(f"👋 Checked out at {current_time}")
            else:
                st.warning("❗ No check-in record found.")

    cursor.close()
    connection.close()
