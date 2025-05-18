import streamlit as st
import pandas as pd
from db_connection import get_connection  # ✅ استدعاء الاتصال من الملف الموحد

def add_employee2():
    st.title("➕ Add New Employee")

    # مدخلات البيانات
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    national_id = st.text_input("National ID")
    job_title = st.text_input("Job Title")
    salary = st.number_input("Salary", min_value=0)
    passport_number = st.text_input("Passport Number")
    address = st.text_input("Address")
    device_serial = st.text_input("Device Serial")
    mobile_number = st.text_input("Mobile Number")  # ✅ أضفنا رقم الهاتف

    if st.button("Add Employee"):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO employees (
                    first_name, last_name, national_id, job_title,
                    salary, passport_number, address, device_serial, mobile_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                first_name, last_name, national_id, job_title,
                salary, passport_number, address, device_serial, mobile_number
            ))

            connection.commit()
            st.success("✅ Employee added successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

        finally:
            cursor.close()
            connection.close()

    