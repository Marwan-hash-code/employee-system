import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
from db_connection import get_connection  # ✅ الاتصال الموحد

def view_invoices2():
    st.title("📜 All Invoices")

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Load all invoices
        cursor.execute("SELECT * FROM invoices ORDER BY invoice_date DESC")
        invoices = cursor.fetchall()

        if not invoices:
            st.info("No invoices found.")
            return

        all_invoice_data = []

        for invoice in invoices:
            with st.expander(f"Invoice #{invoice['id']} - {invoice['invoice_date'].strftime('%Y-%m-%d %H:%M')}"):
                st.write(f"**Customer:** {invoice['customer_name'] or 'N/A'}")
                st.write(f"**Total Amount:** QAR {invoice['total_amount']:.2f}")
                st.write(f"**Payment Method:** {invoice['payment_method']}")
                st.write(f"**Notes:** {invoice['notes'] or '---'}")

                # Load invoice items
                cursor.execute("""
                    SELECT i.item_name, ii.quantity, ii.price, ii.total
                    FROM invoice_items ii
                    JOIN inventory_items i ON ii.item_id = i.id
                    WHERE ii.invoice_id = %s
                """, (invoice['id'],))
                items = cursor.fetchall()
                all_invoice_data.append((invoice, items))

                item_df = pd.DataFrame(items)
                st.dataframe(item_df, use_container_width=True)

                if st.button(f"📄 Export Invoice #{invoice['id']} to PDF", key=f"pdf_{invoice['id']}"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt=f"Invoice #{invoice['id']}", ln=True, align="C")
                    pdf.ln(5)
                    pdf.cell(200, 10, txt=f"Date: {invoice['invoice_date']}", ln=True)
                    pdf.cell(200, 10, txt=f"Customer: {invoice['customer_name'] or 'N/A'}", ln=True)
                    pdf.cell(200, 10, txt=f"Payment: {invoice['payment_method']}", ln=True)
                    pdf.cell(200, 10, txt=f"Notes: {invoice['notes'] or '-'}", ln=True)
                    pdf.ln(5)

                    for item in items:
                        line = f"{item['item_name']} | Qty: {item['quantity']} | Price: QAR {item['price']} | Total: QAR {item['total']}"
                        pdf.cell(200, 10, txt=line, ln=True)

                    pdf.ln(5)
                    pdf.cell(200, 10, txt=f"Total Amount: QAR {invoice['total_amount']:.2f}", ln=True)

                    pdf_file = f"invoice_{invoice['id']}.pdf"
                    pdf.output(pdf_file)

                    with open(pdf_file, "rb") as file:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=file,
                            file_name=pdf_file,
                            mime="application/pdf"
                        )

                    os.remove(pdf_file)

        # ✅ Export all invoices together
        if all_invoice_data and st.button("📥 Export ALL Invoices to One PDF"):
            merged_pdf = FPDF()
            merged_pdf.set_font("Arial", size=12)

            for invoice, items in all_invoice_data:
                merged_pdf.add_page()
                merged_pdf.cell(200, 10, txt=f"Invoice #{invoice['id']}", ln=True, align="C")
                merged_pdf.ln(5)
                merged_pdf.cell(200, 10, txt=f"Date: {invoice['invoice_date']}", ln=True)
                merged_pdf.cell(200, 10, txt=f"Customer: {invoice['customer_name'] or 'N/A'}", ln=True)
                merged_pdf.cell(200, 10, txt=f"Payment: {invoice['payment_method']}", ln=True)
                merged_pdf.cell(200, 10, txt=f"Notes: {invoice['notes'] or '-'}", ln=True)
                merged_pdf.ln(5)

                for item in items:
                    line = f"{item['item_name']} | Qty: {item['quantity']} | Price: QAR {item['price']} | Total: QAR {item['total']}"
                    merged_pdf.cell(200, 10, txt=line, ln=True)

                merged_pdf.ln(5)
                merged_pdf.cell(200, 10, txt=f"Total Amount: QAR {invoice['total_amount']:.2f}", ln=True)

            full_path = "all_invoices.pdf"
            merged_pdf.output(full_path)

            with open(full_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download ALL Invoices PDF",
                    data=file,
                    file_name="all_invoices.pdf",
                    mime="application/pdf"
                )

            os.remove(full_path)

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        cursor.close()
        connection.close()
