import streamlit as st
from fpdf import FPDF
import os
from db_connection import get_connection  # ✅ الاتصال الموحد

def stock_in2():
    st.title("📥 Stock In")

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Get all items
        cursor.execute("SELECT id, item_name, quantity FROM inventory_items")
        items = cursor.fetchall()

        if not items:
            st.warning("No items found in inventory.")
            return

        item_names = [f"{item['item_name']} (Current: {item['quantity']})" for item in items]
        selected_index = st.selectbox("Select Item", range(len(item_names)), format_func=lambda i: item_names[i])
        selected_item = items[selected_index]

        qty_to_add = st.number_input("Quantity to add", min_value=1, step=1)

        if st.button("➕ Add to Stock"):
            # 1. Update inventory_items
            cursor.execute("UPDATE inventory_items SET quantity = quantity + %s WHERE id = %s",
                           (qty_to_add, selected_item['id']))
            connection.commit()

            # 2. Log into stock_movements
            cursor.execute("""
                INSERT INTO stock_movements (item_id, movement_type, quantity)
                VALUES (%s, 'IN', %s)
            """, (selected_item['id'], qty_to_add))
            connection.commit()

            st.success(f"✅ {qty_to_add} units added to '{selected_item['item_name']}'.")

        st.markdown("---")

        # ✅ PDF Report for Stock IN
        if st.button("📄 Generate Stock IN PDF Report"):
            cursor.execute("""
                SELECT i.item_name, m.quantity, m.timestamp
                FROM stock_movements m
                JOIN inventory_items i ON m.item_id = i.id
                WHERE m.movement_type = 'IN'
                ORDER BY m.timestamp DESC
            """)
            records = cursor.fetchall()

            if not records:
                st.info("No stock IN records found.")
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Stock IN Report", ln=True, align="C")
            pdf.ln(10)

            for row in records:
                line = f"{row['item_name']} - Qty: {row['quantity']} - Date: {row['timestamp'].strftime('%Y-%m-%d %H:%M')}"
                pdf.cell(200, 10, txt=line, ln=True)

            output_path = "stock_in_report.pdf"
            pdf.output(output_path)

            with open(output_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=file,
                    file_name="stock_in_report.pdf",
                    mime="application/pdf"
                )

            os.remove(output_path)

    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        connection.close()
