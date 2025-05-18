import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
from db_connection import get_connection  # ✅ الاتصال الموحد

def attendance_report2():
    st.title("📊 Attendance Report")

    try:
        connection = get_connection()
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

        # ✅ حذف الصفوف اللي مفيهاش Check-out
        df = df[df["Check-out"].notna()]

        # ✅ حساب مدة العمل
        df["Worked Duration"] = (
            df["Check-out"] - df["Check-in"]
        ).apply(lambda delta: f"{int(delta.seconds // 3600):02d}:{int((delta.seconds % 3600) // 60):02d}")

        df["Full Name"] = df["First Name"] + " " + df["Last Name"]
        employee_list = df["Full Name"].unique().tolist()
        selected_employee = st.selectbox("🔍 Select Employee", employee_list)

        filtered_df = df[df["Full Name"] == selected_employee]

        # ✅ تلوين السطور الأقل من 8 ساعات
        def highlight_short_hours(duration_str):
            hours, minutes = map(int, duration_str.split(":"))
            return "background-color: red" if hours < 8 else ""

        st.dataframe(filtered_df.style.applymap(highlight_short_hours, subset=["Worked Duration"]))

        # ✅ PDF report
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

        # ✅ Excel Export لكل الموظفين
        if st.button("⬇️ Download Full Excel Report"):
            excel_df = df[["Full Name", "Check-in", "Check-out", "Worked Duration"]]
            excel_path = "attendance_full.xlsx"
            excel_df.to_excel(excel_path, index=False)

            with open(excel_path, "rb") as f:
                st.download_button(
                    label="📥 Download Excel File",
                    data=f,
                    file_name="attendance_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            os.remove(excel_path)

    except Exception as e:
        st.error(f"❌ Error loading attendance report: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
