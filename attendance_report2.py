import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from fpdf import FPDF
import os

def attendance_report2():
    st.title("📊 Attendance Report")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MARWan99@",
            database="company_system"
        )
        cursor = connection.cursor()

        query = """
        SELECT e.first_name, e.last_name, a.check_in, a.check_out
        FROM employees e
        JOIN attendance a ON e.id = a.employee_id
        ORDER BY a.check_in DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=["First Name", "Last Name", "Check-in", "Check-out"])
        df["Check-in"] = pd.to_datetime(df["Check-in"])
        df["Check-out"] = pd.to_datetime(df["Check-out"])
        df["Worked Duration"] = (
            df["Check-out"] - df["Check-in"]
        ).apply(lambda delta: f"{delta.seconds // 3600:02d}:{(delta.seconds % 3600) // 60:02d}")

        df["Full Name"] = df["First Name"] + " " + df["Last Name"]
        employee_list = df["Full Name"].unique().tolist()
        selected_employee = st.selectbox("🔍 Select Employee", employee_list)

        filtered_df = df[df["Full Name"] == selected_employee]

        # ✅ تلوين السطور الأقل من 8 ساعات
        def highlight_short_hours(duration_str):
            hours, minutes = map(int, duration_str.split(":"))
            return "background-color: red" if hours < 8 else ""

        st.dataframe(filtered_df.style.applymap(highlight_short_hours, subset=["Worked Duration"]))

        # ✅ رسم بياني بسيط (بالساعات فقط)
        filtered_df["Hours"] = filtered_df["Worked Duration"].apply(lambda x: int(x.split(":")[0]))
        fig = px.bar(
            filtered_df,
            x="Check-in",
            y="Hours",
            title=f"Monthly Work Hours for {selected_employee}",
            labels={"Check-in": "Date", "Hours": "Hours"},
        )
        st.plotly_chart(fig)

        # ✅ توليد تقرير PDF
        if st.button("📄 Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Attendance Report for {selected_employee}", ln=True, align="C")
            pdf.ln(10)

            for index, row in filtered_df.iterrows():
                date = row["Check-in"].strftime("%Y-%m-%d")
                pdf.cell(200, 10, txt=f"{date} | {row['Worked Duration']} hrs", ln=True)

            output_path = "attendance_report.pdf"
            pdf.output(output_path)

            with open(output_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=file,
                    file_name="attendance_report.pdf",
                    mime="application/pdf"
                )

            os.remove(output_path)

    except Exception as e:
        st.error(f"❌ Error loading attendance report: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
