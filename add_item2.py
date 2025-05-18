import streamlit as st
from datetime import date
from db_connection import get_connection  # ✅ الاتصال الموحد

def add_item2():
    st.title("📦 Add New Inventory Item")

    item_name = st.text_input("Item Name")
    item_code = st.text_input("Item Code / Barcode")
    category = st.text_input("Category")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    min_threshold = st.number_input("Minimum Alert Threshold", min_value=0, step=1)
    price = st.number_input("Price per Unit", min_value=0.0, step=0.01)
    country = st.text_input("Country of Origin")
    expiry_date = st.date_input("Date of Expiry", value=date.today())  # ✅ New field

    if st.button("➕ Add Item"):
        if item_name and item_code:
            try:
                connection = get_connection()
                cursor = connection.cursor()
                sql = """
                    INSERT INTO inventory_items (
                        item_name, item_code, category,
                        quantity, min_threshold, price, country_of_origin, date_of_expiry
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    item_name, item_code, category,
                    quantity, min_threshold, price, country, expiry_date
                )
                cursor.execute(sql, values)
                connection.commit()
                st.success("✅ Item added successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            st.warning("⚠️ Please enter both Item Name and Code.")
