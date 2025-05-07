import streamlit as st
import mysql.connector
import pandas as pd

def view_employees2():
    st.title("📋 All Employees")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MARWan99@",
            database="company_system"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]

        df = pd.DataFrame(rows, columns=columns)
        st.dataframe(df, use_container_width=True)

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
