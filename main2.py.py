import streamlit as st
from login2 import login2
from dashboard2 import dashboard2

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login2()
    else:
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Go to:", ["Dashboard"])

        if choice == "Dashboard":
            dashboard2()

if __name__ == "__main__":
    main()

