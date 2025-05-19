import streamlit as st
st.set_page_config(page_title="Grant MySQL Remote Access", layout="wide")

import mysql.connector
import os

def grant_access():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            port=int(os.environ.get("DB_PORT", 3306))  # افتراضيًا 3306 لو مش موجود
        )

        cursor = connection.cursor()

        # أمر السماح لأي IP بالاتصال
        cursor.execute(f"""
            GRANT ALL PRIVILEGES ON *.* TO '{os.environ.get("DB_USER")}'@'%' IDENTIFIED BY '{os.environ.get("DB_PASSWORD")}';
        """)
        cursor.execute("FLUSH PRIVILEGES;")
        connection.commit()

        st.success("✅ تم تفعيل الاتصال من أي IP بنجاح.")
    
    except Exception as e:
        st.error("❌ حدث خطأ أثناء تنفيذ الأمر:")
        st.code(str(e))  # عرض الخطأ بالتفصيل
    
    finally:
        try:
            if connection.is_connected():
                cursor.close()
                connection.close()
        except:
            pass

# واجهة الصفحة
st.title("Grant MySQL Remote Access")

st.write("اضغط الزر لتفعيل الاتصال من أي IP بقاعدة البيانات (مثلاً من Render).")

if st.button("Grant Access"):
    grant_access()
