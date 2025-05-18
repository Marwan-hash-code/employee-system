import streamlit as st
import mysql.connector
from db_connection import get_connection

def remove_employee2():
    st.title("🗑️ Remove Employee")

    connection = get_connection()
    cursor = connection.cursor()

    # ✅ Fetch employees
    cursor.execute("SELECT id, first_name, last_name FROM employees")
    employees = cursor.fetchall()

    if not employees:
        st.info("No employees found.")
        return

    # ✅ Bulk deletion section
    st.subheader("🧹 Remove Multiple Employees")

    employee_dict = {f"{emp[1]} {emp[2]} (ID: {emp[0]})": emp[0] for emp in employees}
    selected_multi = st.multiselect("Select employees to delete:", list(employee_dict.keys()))

    user_role = st.session_state.get("user_role", "")
    confirm_multi_delete = st.checkbox("✅ I confirm I want to delete all related data for selected employees")

    if selected_multi:
        if st.button("🧨 Delete Selected Employees"):
            try:
                for name in selected_multi:
                    emp_id = employee_dict[name]

                    if confirm_multi_delete and user_role in ["admin", "developer"]:
                        # Full deletion
                        cursor.execute("DELETE FROM attendance WHERE employee_id = %s", (emp_id,))
                        cursor.execute("DELETE FROM devices WHERE employee_id = %s", (emp_id,))
                        cursor.execute("DELETE FROM performance WHERE employee_id = %s", (emp_id,))
                        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
                    else:
                        # Safe deletion (only if no related data exists)
                        cursor.execute("SELECT COUNT(*) FROM attendance WHERE employee_id = %s", (emp_id,))
                        attendance_count = cursor.fetchone()[0]

                        cursor.execute("SELECT COUNT(*) FROM devices WHERE employee_id = %s", (emp_id,))
                        devices_count = cursor.fetchone()[0]

                        cursor.execute("SELECT COUNT(*) FROM performance WHERE employee_id = %s", (emp_id,))
                        performance_count = cursor.fetchone()[0]

                        total_related = attendance_count + devices_count + performance_count

                        if total_related > 0:
                            st.warning(f"{name} has related data. Skipping.")
                        else:
                            cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
                
                connection.commit()
                st.success("✅ Selected employees were deleted according to the selected option.")
                st.rerun()

            except Exception as e:
                st.error(f"Unexpected error: {e}")

    st.markdown("---")
    st.subheader("🧍 Remove Single Employee")

    # ✅ Single deletion
    selected = st.selectbox("Select an employee to remove:", employees, format_func=lambda x: f"{x[1]} {x[2]}")

    if selected:
        emp_id = selected[0]
        emp_name = f"{selected[1]} {selected[2]}"

        st.warning(f"You selected to remove **{emp_name}**")

        if st.button("❌ Remove from employee table only"):
            try:
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE employee_id = %s", (emp_id,))
                attendance_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM devices WHERE employee_id = %s", (emp_id,))
                devices_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM performance WHERE employee_id = %s", (emp_id,))
                performance_count = cursor.fetchone()[0]

                total_related = attendance_count + devices_count + performance_count

                if total_related > 0:
                    st.warning("This employee has related data (e.g. attendance, devices, performance). Please use the full delete option below.")
                else:
                    cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
                    connection.commit()
                    st.success(f"{emp_name} removed from employees table.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

        if user_role in ["admin", "developer"]:
            confirm_delete = st.checkbox("✅ I confirm I want to delete all related data")

            if confirm_delete:
                if st.button("🧨 Delete employee and all related data"):
                    try:
                        cursor.execute("DELETE FROM attendance WHERE employee_id = %s", (emp_id,))
                        cursor.execute("DELETE FROM devices WHERE employee_id = %s", (emp_id,))
                        cursor.execute("DELETE FROM performance WHERE employee_id = %s", (emp_id,))
                        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
                        connection.commit()

                        st.success(f"✅ All data for {emp_name} has been permanently deleted.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.info("Check the box to confirm deletion of all related data.")
