import streamlit as st
from db_connection import get_connection  # ✅ الاتصال الموحد

def edit_users2():
    st.title("🛠️ Edit User Information")

    # Connect to the database
    connection = get_connection()
    cursor = connection.cursor()

    # ✅ Fetch users excluding developer
    cursor.execute("SELECT username FROM users WHERE username != 'marwan_zynox_master'")
    users = [row[0] for row in cursor.fetchall()]

    if users:
        selected_user = st.selectbox("Select User", users)

        cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (selected_user,))
        user_data = cursor.fetchone()

        new_username = st.text_input("New Username", user_data[0])
        new_password = st.text_input("New Password", user_data[1])
        
        # ✅ Only real roles
        all_roles = ["admin", "employee", "inventory", "developer"]
        new_role = st.selectbox("Role", all_roles, index=all_roles.index(user_data[2]))

        if st.button("💾 Save Changes"):
            cursor.execute("""
                UPDATE users
                SET username = %s, password = %s, role = %s
                WHERE username = %s
            """, (new_username, new_password, new_role, selected_user))
            connection.commit()
            st.success("✅ User information updated successfully!")

    else:
        st.info("No users found.")

    cursor.close()
    connection.close()
