import streamlit as st
import mysql.connector
import pandas as pd

def view_employees2():
    st.title("👨‍💼 View Employees")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MARWan99@",
        database="company_system"
    )
    cursor = connection.cursor()

    # ✅ جلب البيانات
    cursor.execute("""
        SELECT first_name, last_name, national_id, job_title,
               salary, passport_number, address, device_serial, mobile_number
        FROM employees
    """)
    results = cursor.fetchall()

    df = pd.DataFrame(results, columns=[
        "First Name", "Last Name", "National ID", "Job Title",
        "Salary", "Passport Number", "Address", "Device Serial", "Mobile Number"
    ])

    # ✅ مربع البحث
    search_term = st.text_input("🔍 Search by name or job title")

    if search_term:
        df = df[
            df["First Name"].str.contains(search_term, case=False, na=False) |
            df["Last Name"].str.contains(search_term, case=False, na=False) |
            df["Job Title"].str.contains(search_term, case=False, na=False)
        ]

    st.dataframe(df)

    cursor.close()
    connection.close()
