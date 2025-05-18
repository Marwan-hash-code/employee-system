import streamlit as st
from datetime import datetime
from db_connection import get_connection  # ✅ الاتصال الموحد

def add_invoice2():
    st.title("🧾 Add New Invoice")

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Get all available items
        cursor.execute("SELECT id, item_name, price FROM inventory_items")
        items = cursor.fetchall()
        item_names = [f"{item['item_name']} (QAR {item['price']})" for item in items]

        customer_name = st.text_input("Customer Name")
        payment_method = st.selectbox("Payment Method", ["Cash", "Credit", "Other"])
        notes = st.text_area("Notes")

        st.subheader("🧺 Select Items")
        selected_items = []

        for i, item in enumerate(items):
            with st.expander(f"{item['item_name']}"):
                qty = st.number_input(f"Quantity for {item['item_name']}", min_value=0, step=1, key=f"qty_{i}")
                if qty > 0:
                    selected_items.append({
                        "item_id": item["id"],
                        "name": item["item_name"],
                        "price": item["price"],
                        "quantity": qty,
                        "total": item["price"] * qty
                    })

        total_amount = sum(x["total"] for x in selected_items)
        st.markdown(f"### 💰 Total: **QAR {total_amount:.2f}**")

        if st.button("✅ Confirm Invoice"):
            # Insert invoice
            cursor.execute("""
                INSERT INTO invoices (invoice_date, customer_name, total_amount, payment_method, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (datetime.now(), customer_name, total_amount, payment_method, notes))
            invoice_id = cursor.lastrowid

            # Insert items
            for item in selected_items:
                cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, item_id, quantity, price, total)
                    VALUES (%s, %s, %s, %s, %s)
                """, (invoice_id, item["item_id"], item["quantity"], item["price"], item["total"]))

            connection.commit()
            st.success("✅ Invoice created successfully!")

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        cursor.close()
        connection.close()
