import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from db_connection import get_connection
from io import BytesIO

def payroll_dashboard2():
    st.title("💼 Payroll Dashboard")

    # ✅ Connect to database
    connection = get_connection()
    cursor = connection.cursor()

    # ✅ Fetch manager settings
    cursor.execute("""
        SELECT work_days_per_week, work_hours_per_day, 
               penalty_per_late_day, bonus_per_good_attendance 
        FROM settings LIMIT 1
    """)
    settings = cursor.fetchone()
    if settings:
        work_days_per_week, work_hours_per_day, penalty_per_late_day, bonus_per_good_attendance = settings
    else:
        st.error("⚠️ Manager settings not found in the database.")
        return

    # ✅ Fetch employees
    cursor.execute("SELECT id, first_name, last_name, salary FROM employees")
    employees = cursor.fetchall()

    data = []

    for emp_id, first, last, salary in employees:
        # Get attendance days
        cursor.execute("SELECT check_in FROM attendance WHERE employee_id = %s", (emp_id,))
        check_ins = cursor.fetchall()

        total_attendance = len(set([c[0].date() for c in check_ins if c[0] is not None]))

        today = datetime.today().date()
        total_working_days = work_days_per_week * 4  # Approximate 4 weeks per month

        # Count late check-ins (after 9:00 AM)
        late_days = sum(
            1 for c in check_ins 
            if c[0] is not None and c[0].time() > datetime.strptime("09:00:00", "%H:%M:%S").time()
        )

        absent_days = total_working_days - total_attendance
        total_penalty = late_days * penalty_per_late_day
        total_bonus = bonus_per_good_attendance if total_attendance >= total_working_days else 0
        final_salary = salary - total_penalty + total_bonus

        data.append({
            "Employee Name": f"{first} {last}",
            "Basic Salary": salary,
            "Attendance Days": total_attendance,
            "Absent Days": absent_days,
            "Late Days": late_days,
            "Penalty": total_penalty,
            "Bonus": total_bonus,
            "Final Salary": final_salary
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # ✅ Download as Excel
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Payroll Report')
        return output.getvalue()

    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="📥 Download Payroll Report (Excel)",
        data=excel_data,
        file_name="payroll_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
