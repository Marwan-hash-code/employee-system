import streamlit as st
from db_connection import get_connection  # ✅ الاتصال الموحد

def dev_settings2():
    st.title("🛠️ Developer Settings")

    # ✅ Back button
    if st.button("⬅️ Back to System"):
        st.experimental_rerun()

    # Connect to the database
    connection = get_connection()
    cursor = connection.cursor()

    # Get current developer account
    cursor.execute("SELECT username, password FROM users WHERE role = 'developer'")
    dev_user = cursor.fetchone()

    if dev_user:
        current_username = dev_user[0]
        current_password = dev_user[1]

        st.info("🔽 Current Credentials:")
        st.text(f"👤 Username: {current_username}")
        st.text(f"🔑 Password: {current_password}")

        st.markdown("---")

        new_username = st.text_input("New Username", value=current_username)
        new_password = st.text_input("New Password", value=current_password)

        if st.button("💾 Save Changes"):
            cursor.execute("""
                UPDATE users
                SET username = %s, password = %s
                WHERE role = 'developer'
            """, (new_username, new_password))
            connection.commit()
            st.success("✅ Developer credentials updated successfully!")

    else:
        st.error("❌ Developer account not found.")

    cursor.close()
    connection.close()
