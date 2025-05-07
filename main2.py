import streamlit as st
from login2 import login2
from dashboard2 import dashboard2
from add_employee2 import add_employee2
from view_employees2 import view_employees2
from checkin2 import checkin2         # ✅ Check-In
from checkout2 import checkout2       # ✅ Check-Out
from attendance_report2 import attendance_report2  # ✅ Attendance Report
from remove_employee2 import remove_employee2       # ✅ Remove Employee

def main():
    st.set_page_config(page_title="Employee Management System", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login2()
    else:
        st.sidebar.title("Navigation")
        option = st.sidebar.radio("Go to", [
            "Dashboard",
            "Add Employee",
            "View Employees",
            "Check-In",          # ✅ Check-In
            "Check-Out",         # ✅ Check-Out
            "Attendance Report", # ✅ Attendance Report
            "Remove Employee",   # ✅ Remove Employee
            "Logout"
        ])

        if option == "Dashboard":
            dashboard2()
        elif option == "Add Employee":
            add_employee2()
        elif option == "View Employees":
            view_employees2()
        elif option == "Check-In":
            checkin2()
        elif option == "Check-Out":
            checkout2()
        elif option == "AI Analysis":
            ai_analysis2()
        elif option == "Attendance Report":
            attendance_report2()
        elif option == "Remove Employee":
            remove_employee2()
        elif option == "Logout":
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
