import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from db_connection import get_connection  # ✅ الاتصال الموحد

def stock_history2():
    st.title("📑 Stock Movement History")

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Get stock movements with item names
        cursor.execute("""
            SELECT i.item_name, m.movement_type, m.quantity, m.movement_date
            FROM stock_movements m
            JOIN inventory_items i ON m.item_id = i.id
            ORDER BY m.movement_date DESC
        """)
        rows = cursor.fetchall()

        if rows:
            df = pd.DataFrame(rows, columns=["Item Name", "Type", "Quantity", "Date"])
            st.dataframe(df, use_container_width=True)

            # ✅ زر توليد PDF
            if st.button("📄 Generate Full Stock Movement PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Stock Movement Report", ln=True, align="C")
                pdf.ln(10)

                for _, row in df.iterrows():
                    line = f"{row['Date']} - {row['Type']} - {row['Item Name']} - Qty: {row['Quantity']}"
                    pdf.cell(200, 10, txt=line, ln=True)

                output_path = "stock_history_report.pdf"
                pdf.output(output_path)

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=file,
                        file_name="stock_history_report.pdf",
                        mime="application/pdf"
                    )

                os.remove(output_path)

        else:
            st.info("No stock movements recorded yet.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        connection.close()
