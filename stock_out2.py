import streamlit as st
from fpdf import FPDF
import os
from db_connection import get_connection  # ✅ الاتصال الموحد

def stock_out2():
    st.title("📤 Stock Out")

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Get items
        cursor.execute("SELECT id, item_name, quantity FROM inventory_items")
        items = cursor.fetchall()

        if not items:
            st.warning("No items found.")
            return

        item_names = [f"{item['item_name']} (Available: {item['quantity']})" for item in items]
        selected_index = st.selectbox("Select Item", range(len(item_names)), format_func=lambda i: item_names[i])
        selected_item = items[selected_index]

        qty_to_remove = st.number_input("Quantity to remove", min_value=1, step=1)

        if st.button("➖ Remove from Stock"):
            if qty_to_remove > selected_item['quantity']:
                st.error("❌ Not enough quantity available.")
            else:
                # 1. Update inventory
                cursor.execute(
                    "UPDATE inventory_items SET quantity = quantity - %s WHERE id = %s",
                    (qty_to_remove, selected_item['id'])
                )
                connection.commit()

                # 2. Record movement
                cursor.execute("""
                    INSERT INTO stock_movements (item_id, movement_type, quantity)
                    VALUES (%s, 'OUT', %s)
                """, (selected_item['id'], qty_to_remove))
                connection.commit()

                st.success(f"✅ {qty_to_remove} units removed from '{selected_item['item_name']}'.")

        st.markdown("---")

        # ✅ PDF Report of all Stock OUT history
        if st.button("📄 Generate Stock OUT PDF Report"):
            cursor.execute("""
                SELECT i.item_name, m.quantity, m.timestamp
                FROM stock_movements m
                JOIN inventory_items i ON m.item_id = i.id
                WHERE m.movement_type = 'OUT'
                ORDER BY m.timestamp DESC
            """)
            rows = cursor.fetchall()

            if not rows:
                st.info("No stock OUT records to export.")
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Stock OUT Report", ln=True, align="C")
            pdf.ln(10)

            for row in rows:
                line = f"{row['item_name']} - Qty: {row['quantity']} - Date: {row['timestamp'].strftime('%Y-%m-%d %H:%M')}"
                pdf.cell(200, 10, txt=line, ln=True)

            output_path = "stock_out_report.pdf"
            pdf.output(output_path)

            with open(output_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=file,
                    file_name="stock_out_report.pdf",
                    mime="application/pdf"
                )

            os.remove(output_path)

    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        connection.close()
