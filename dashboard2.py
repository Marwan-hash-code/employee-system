import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt

def dashboard2():
    st.title("📊 Dashboard")

    try:
        # الاتصال بقاعدة البيانات
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MARWan99@",  # عدلها لو غيرت الباسورد
            database="company_system"
        )
        cursor = conn.cursor()

        # عدد الموظفين
        cursor.execute("SELECT COUNT(*) FROM employees")
        total_employees = cursor.fetchone()[0]
        st.subheader("Total Employees")
        st.write(total_employees)

        # متوسط المرتب
        cursor.execute("SELECT AVG(salary) FROM employees")
        avg_salary = cursor.fetchone()[0] or 0
        st.subheader("Average Salary")
        st.write(f"{avg_salary:.2f} EGP")

        # رسم بياني للوظائف وعدد الموظفين
        cursor.execute("SELECT job_title, COUNT(*) FROM employees GROUP BY job_title")
        data = cursor.fetchall()
        if data:
            job_titles = [row[0] for row in data]
            counts = [row[1] for row in data]

            fig, ax = plt.subplots()
            ax.bar(job_titles, counts)
            plt.xticks(rotation=45)
            ax.set_xlabel("Job Title")
            ax.set_ylabel("Number of Employees")
            ax.set_title("Employees by Job Title")

            st.pyplot(fig)

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")
