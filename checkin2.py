import streamlit as st
import mysql.connector
from datetime import datetime

def checkin2():
    st.title("🟢 Check-In")

    # الاتصال بقاعدة البيانات
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

    # تجهيز القائمة مع اسم + وظيفة
    employee_dict = {
        f"{emp[1]} {emp[2]} - {emp[3]}": emp[0]
        for emp in employees
    }

    # مربع البحث
    selected = st.selectbox("🔍 Search and select your name:", list(employee_dict.keys()))

    if selected:
        employee_id = employee_dict[selected]

        if st.button("✅ Check In"):
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute("""
                INSERT INTO attendance (employee_id, check_in)
                VALUES (%s, %s)
            """, (employee_id, current_time))
            connection.commit()

            st.success(f"✅ Checked in at {current_time}")

    cursor.close()
    connection.close()
