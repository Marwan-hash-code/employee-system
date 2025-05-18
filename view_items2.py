import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from db_connection import get_connection  # ✅ الاتصال الموحد

def view_items2():
    st.title("📋 Inventory Items List")

    try:
        # Connect to database
        connection = get_connection()
        cursor = connection.cursor()

        # Fetch full item list
        cursor.execute("""
            SELECT item_name, item_code, category, quantity, min_threshold,
                   price, country_of_origin, date_of_expiry, date_added
            FROM inventory_items
        """)
        rows = cursor.fetchall()

        columns = [
            "Item Name", "Item Code", "Category", "Quantity", "Min Threshold",
            "Price", "Country of Origin", "Date of Expiry", "Date Added"
        ]
        df = pd.DataFrame(rows, columns=columns)

        st.dataframe(df, use_container_width=True)

        # ✅ Generate PDF
        if st.button("📄 Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Inventory Report", ln=True, align="C")
            pdf.ln(10)

            for _, row in df.iterrows():
                line = f"{row['Item Name']} | Qty: {row['Quantity']} | Price: {row['Price']} | Country: {row['Country of Origin']}"
                if row["Date of Expiry"]:
                    line += f" | Expiry: {row['Date of Expiry']}"
                pdf.cell(200, 10, txt=line, ln=True)

            output_path = "inventory_report.pdf"
            pdf.output(output_path)

            with open(output_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=file,
                    file_name="inventory_report.pdf",
                    mime="application/pdf"
                )

            os.remove(output_path)

    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        connection.close()
