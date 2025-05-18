import streamlit as st
import json
import os

SETTINGS_FILE = "payroll_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def payroll_settings2():
    st.title("⚙️ Payroll Settings")

    current_settings = load_settings()

    # عدد أيام الإجازة السنوية
    annual_leave = st.number_input(
        "Annual Leave Days", min_value=0, max_value=60,
        value=current_settings.get("annual_leave", 21)
    )

    # أيام العمل في الأسبوع
    st.markdown("**Working Days**")
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    selected_days = st.multiselect(
        "Select working days", weekdays,
        default=current_settings.get("working_days", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"])
    )

    # خصم الغياب
    enable_absence_deduction = st.checkbox(
        "Enable Absence Deduction", value=current_settings.get("enable_absence_deduction", True)
    )
    absence_deduction = 0
    if enable_absence_deduction:
        absence_deduction = st.number_input(
            "Deduction per Absence (QAR)", min_value=0,
            value=current_settings.get("absence_deduction", 100)
        )

    # خصم التأخير
    enable_late_deduction = st.checkbox(
        "Enable Late Deduction", value=current_settings.get("enable_late_deduction", True)
    )
    late_deduction = 0
    if enable_late_deduction:
        late_deduction = st.number_input(
            "Deduction per Hour Late (QAR)", min_value=0,
            value=current_settings.get("late_deduction", 10)
        )

    # الحافز
    enable_bonus = st.checkbox(
        "Enable Monthly Bonus", value=current_settings.get("enable_bonus", True)
    )
    bonus_value = 0
    if enable_bonus:
        bonus_value = st.number_input(
            "Bonus for Full Attendance (QAR)", min_value=0,
            value=current_settings.get("bonus_value", 300)
        )

    if st.button("💾 Save Settings"):
        settings = {
            "annual_leave": annual_leave,
            "working_days": selected_days,
            "enable_absence_deduction": enable_absence_deduction,
            "absence_deduction": absence_deduction,
            "enable_late_deduction": enable_late_deduction,
            "late_deduction": late_deduction,
            "enable_bonus": enable_bonus,
            "bonus_value": bonus_value,
        }
        save_settings(settings)
        st.success("✅ Settings saved successfully!")

# شغّل الصفحة لما تكون مستقلة
if __name__ == "__main__":
    payroll_settings2()
