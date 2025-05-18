import streamlit as st
import pandas as pd
from datetime import datetime, date
from db_connection import get_connection  # ✅ الاتصال الموحد

def manage_items2():
    st.title("🛠️ Manage Inventory Items")

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch items
        cursor.execute("SELECT * FROM inventory_items")
        items = cursor.fetchall()

        if not items:
            st.info("No items found.")
            return

        for item in items:
            with st.expander(f"{item['item_name']} - {item['item_code']}"):
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Quantity:** {item['quantity']}")
                st.write(f"**Min Threshold:** {item['min_threshold']}")
                st.write(f"**Price:** {item.get('price', 'N/A')}")
                st.write(f"**Country of Origin:** {item.get('country_of_origin', 'N/A')}")
                st.write(f"**Date of Expiry:** {item.get('date_of_expiry', 'N/A')}")
                st.write(f"**Date Added:** {item['date_added']}")

                # Edit form
                with st.form(f"edit_form_{item['id']}"):
                    new_name = st.text_input("Item Name", value=item['item_name'])
                    new_code = st.text_input("Item Code", value=item['item_code'])
                    new_cat = st.text_input("Category", value=item['category'])
                    new_qty = st.number_input("Quantity", value=int(item['quantity']), min_value=0, step=1)
                    new_min = st.number_input("Min Threshold", value=int(item['min_threshold']), min_value=0, step=1)
                    new_price = st.number_input("Price", value=float(item.get('price') or 0.0), min_value=0.0, step=0.01)
                    new_country = st.text_input("Country of Origin", value=item.get('country_of_origin') or "")
                    
                    # ✅ safely handle date input
                    expiry_val = item.get('date_of_expiry')
                    if isinstance(expiry_val, str):
                        expiry_val = datetime.strptime(expiry_val, "%Y-%m-%d").date()
                    new_expiry = st.date_input("Date of Expiry", value=expiry_val or date.today())

                    submitted = st.form_submit_button("Save Changes")
                    if submitted:
                        update_sql = """
                            UPDATE inventory_items
                            SET item_name=%s, item_code=%s, category=%s,
                                quantity=%s, min_threshold=%s, price=%s,
                                country_of_origin=%s, date_of_expiry=%s
                            WHERE id=%s
                        """
                        values = (
                            new_name, new_code, new_cat,
                            new_qty, new_min, new_price,
                            new_country, new_expiry, item['id']
                        )
                        cursor.execute(update_sql, values)
                        connection.commit()
                        st.success("✅ Item updated successfully.")
                        st.experimental_rerun()

                # Delete button
                if st.button(f"🗑️ Delete Item {item['item_code']}", key=f"delete_{item['id']}"):
                    cursor.execute("DELETE FROM inventory_items WHERE id = %s", (item['id'],))
                    connection.commit()
                    st.warning("❌ Item deleted.")
                    st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        cursor.close()
        connection.close()
