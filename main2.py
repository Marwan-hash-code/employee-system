import streamlit as st
st.set_page_config(page_title="Zynox System", layout="wide")

from datetime import datetime, date, time
import mysql.connector
import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from base64 import b64decode

from login2 import login2
from dashboard2 import dashboard2
from add_employee2 import add_employee2
from view_employees2 import view_employees2
from checkin2 import checkin2
from checkout2 import checkout2
from attendance_report2 import attendance_report2
from remove_employee2 import remove_employee2

from edit_users2 import edit_users2
from dev_settings2 import dev_settings2
from payroll_settings2 import payroll_settings2
from payroll_dashboard2 import payroll_dashboard2
from upload_employees2 import upload_employees2

from add_item2 import add_item2
from view_items2 import view_items2
from manage_items2 import manage_items2
from inventory_dashboard2 import inventory_dashboard2
from stock_in2 import stock_in2
from stock_out2 import stock_out2
from stock_history2 import stock_history2
from add_invoice2 import add_invoice2
from view_invoices2 import view_invoices2

# ✅ شيلنا import grant_access2

def load_license_config():
    try:
        with open("license.json", "r") as f:
            license_data = json.load(f)

        signature = b64decode(license_data.pop("signature"))
        license_json = json.dumps(license_data, separators=(",", ":")).encode()

        with open("public_key.pem", "rb") as f:
            public_key = load_pem_public_key(f.read())

        public_key.verify(
            signature,
            license_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return license_data

    except Exception as e:
        print("❌ Error verifying license:", e)
        return {
            "employee_system": False,
            "inventory_system": False,
            "payroll_system": False,
            "expiry_date": "2000-01-01"
        }

def is_license_expired(expiry_str):
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        return date.today() > expiry_date
    except:
        return True

def main():
    st.set_page_config(page_title="Zynox System", layout="wide")

    license_config = load_license_config()

    if is_license_expired(license_config.get("expiry_date", "")):
        st.error("🚫 License has expired. Please contact your administrator.")
        return

    st.markdown("""
        <style>
            .header-container {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 30px;
            }
            .logo {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 28px;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                text-align: center;
                line-height: 50px;
                margin-right: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            }
            .title {
                font-size: 36px;
                color: #4CAF50;
                font-family: 'Segoe UI', sans-serif;
            }
        </style>
        <div class="header-container">
            <div class="logo">Z</div>
            <div class="title">Zynox System</div>
        </div>
    """, unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login2()
    else:
        if "user_role" not in st.session_state:
            st.warning("No role found. Please log in again.")
            st.session_state.logged_in = False
            st.rerun()

        role = st.session_state.user_role

        if role == "developer":
            st.sidebar.markdown("### Settings")
            if st.sidebar.button("Dev Settings"):
                dev_settings2()
                return

        st.sidebar.title("Main Menu")

        system_options = []
        if license_config.get("employee_system"):
            system_options.append("Employee System")
        if license_config.get("inventory_system"):
            system_options.append("Inventory System")
        if license_config.get("payroll_system") and role in ["admin", "developer"]:
            system_options.append("HR Payroll")

        # ✅ شيلنا Grant DB Access من القايمة
        system_options.append("Logout")

        main_option = st.sidebar.radio("Select System", system_options)

        if main_option == "Employee System":
            employee_pages = []
            if role in ["admin", "developer"]:
                employee_pages = [
                    "Dashboard",
                    "Add Employee",
                    "Upload Employees",
                    "View Employees",
                    "Check-In",
                    "Check-Out",
                    "Attendance Report",
                    "Remove Employee",
                    "Edit Users"
                ]
            elif role in ["employee", "inventory"]:
                employee_pages = ["Check-In", "Check-Out"]

            sub_option = st.sidebar.radio("Go to", employee_pages)
            st.session_state.current_page = sub_option

            if sub_option == "Dashboard":
                dashboard2()
            elif sub_option == "Add Employee":
                add_employee2()
            elif sub_option == "Upload Employees":
                upload_employees2()
            elif sub_option == "View Employees":
                view_employees2()
            elif sub_option == "Check-In":
                checkin2()
            elif sub_option == "Check-Out":
                checkout2()
            elif sub_option == "Attendance Report":
                attendance_report2()
            elif sub_option == "Remove Employee":
                remove_employee2()
            elif sub_option == "Edit Users":
                edit_users2()

        elif main_option == "Inventory System":
            inventory_pages = [
                "Dashboard",
                "Add Item",
                "View Items",
                "Manage Items",
                "Stock In",
                "Stock Out",
                "Stock History",
                "Add Invoice",
                "View Invoices"
            ]
            sub_option = st.sidebar.radio("Inventory Options", inventory_pages)
            st.session_state.current_page = sub_option

            if sub_option == "Dashboard":
                inventory_dashboard2()
            elif sub_option == "Add Item":
                add_item2()
            elif sub_option == "View Items":
                view_items2()
            elif sub_option == "Manage Items":
                manage_items2()
            elif sub_option == "Stock In":
                stock_in2()
            elif sub_option == "Stock Out":
                stock_out2()
            elif sub_option == "Stock History":
                stock_history2()
            elif sub_option == "Add Invoice":
                add_invoice2()
            elif sub_option == "View Invoices":
                view_invoices2()

        elif main_option == "HR Payroll":
            hr_pages = [
                "Payroll Settings",
                "Payroll Dashboard",
                "Upload Employees"
            ]
            sub_option = st.sidebar.radio("HR Options", hr_pages)
            st.session_state.current_page = sub_option

            if sub_option == "Payroll Settings":
                payroll_settings2()
            elif sub_option == "Payroll Dashboard":
                payroll_dashboard2()
            elif sub_option == "Upload Employees":
                upload_employees2()

        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.rerun()

if __name__ == "__main__":
    main()
