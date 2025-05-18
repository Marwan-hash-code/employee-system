import streamlit as st
import pandas as pd
from db_connection import get_connection
from datetime import datetime

def upload_employees2():
    st.title("📥 Upload Employees from Excel")

    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            required_columns = [
                "first_name", "last_name", "id_number", "salary", "passport",
                "residence", "device_serial", "join_time", "job_title"
            ]

            # ✅ Check if required columns exist
            if all(col in df.columns for col in required_columns):
                st.success("✅ File loaded successfully! Preview below:")
                st.dataframe(df)

                if st.button("➕ Add All Employees to Database"):
                    connection = get_connection()
                    cursor = connection.cursor()

                    added = 0
                    for _, row in df.iterrows():
                        try:
                            cursor.execute("""
                                INSERT INTO employees (
                                    first_name, last_name, id_number, salary, passport,
                                    residence, device_serial, join_time, job_title
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                row["first_name"], row["last_name"], row["id_number"], row["salary"],
                                row["passport"], row["residence"], row["device_serial"],
                                row["join_time"] if not pd.isnull(row["join_time"]) else datetime.today().date(),
                                row["job_title"]
                            ))
                            added += 1
                        except Exception as e:
                            st.warning(f"⚠️ Could not add row for {row['first_name']} {row['last_name']}: {e}")

                    connection.commit()
                    st.success(f"✅ {added} employees added successfully.")

            else:
                st.error("❌ Missing required columns in Excel file.")
                st.info(f"Required columns: {', '.join(required_columns)}")

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
