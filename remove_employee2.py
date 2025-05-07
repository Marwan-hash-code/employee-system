import streamlit as st
import mysql.connector
from mysql.connector import Error

def remove_employee2():
    st.title("🗑️ Remove Employee")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MARWan99@",  # ✏️ عدلها لو باسوردك مختلف
            database="company_system"
        )
        cursor = connection.cursor()

        # ✅ جلب الموظفين النشطين فقط
        cursor.execute("SELECT id, first_name, last_name, job_title FROM employees WHERE is_active = 1")
        employees = cursor.fetchall()

        if not employees:
            st.info("No active employees found.")
            return

        # ✅ تجهيز القائمة
        employee_dict = {f"{emp[0]} - {emp[1]} {emp[2]} ({emp[3]})": emp[0] for emp in employees}
        selected = st.selectbox("Select employee to remove:", list(employee_dict.keys()))

        if st.button("❌ Remove Employee"):
            emp_id = employee_dict[selected]
            # ✅ التحديث بدلاً من الحذف
            cursor.execute("UPDATE employees SET is_active = 0 WHERE id = %s", (emp_id,))
            connection.commit()
            st.success("✅ Employee deactivated successfully.")
            st.rerun()

    except Error as e:
        st.error(f"❌ Error removing employee: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
