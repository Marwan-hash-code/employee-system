import streamlit as st
import pandas as pd
from db_connection import get_connection  # ✅ الاتصال الموحد

def inventory_dashboard2():
    st.title("📊 Inventory Dashboard")

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # 1. Total number of items
        cursor.execute("SELECT COUNT(*) AS total_items FROM inventory_items")
        total_items = cursor.fetchone()['total_items']

        # 2. Total quantity
        cursor.execute("SELECT SUM(quantity) AS total_qty FROM inventory_items")
        total_qty = cursor.fetchone()['total_qty'] or 0

        # 3. Low stock items
        cursor.execute("SELECT COUNT(*) AS low_stock FROM inventory_items WHERE quantity < min_threshold")
        low_stock = cursor.fetchone()['low_stock']

        # 4. Latest added item
        cursor.execute("SELECT item_name, quantity FROM inventory_items ORDER BY date_added DESC LIMIT 1")
        latest = cursor.fetchone()

        # 5. List of low stock items
        cursor.execute("SELECT item_name, quantity, min_threshold FROM inventory_items WHERE quantity < min_threshold")
        low_stock_items = cursor.fetchall()
        low_df = pd.DataFrame(low_stock_items)

        # Display
        st.subheader("🔢 Overview")
        st.write(f"**Total Items:** {total_items}")
        st.write(f"**Total Quantity:** {total_qty}")
        st.write(f"**Items Below Minimum Threshold:** {low_stock}")

        if latest:
            st.write(f"**Latest Item Added:** {latest['item_name']} ({latest['quantity']} units)")

        if not low_df.empty:
            st.subheader("⚠️ Low Stock Items")
            st.dataframe(low_df, use_container_width=True)
        else:
            st.success("✅ No low stock items.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        cursor.close()
        connection.close()
