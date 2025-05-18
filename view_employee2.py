import streamlit as st
import mysql.connector
import pandas as pd
from db_connection import get_connection

def view_employees2():
    st.title("👨‍💼 View Employees")

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                first_name, last_name, national_id, job_title,
                salary, passport_number, residence, address, device_serial, appointment_time
            FROM employees
        """)
        data = cursor.fetchall()

        if data:
            df = pd.DataFrame(data, columns=[
                "First Name", "Last Name", "National ID", "Job Title",
                "Salary", "Passport", "Residence", "Address", "Device Serial", "Appointment Time"
            ])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No employees found.")

    except Exception as e:
        st.error(f"❌ Error loading employees: {e}")
