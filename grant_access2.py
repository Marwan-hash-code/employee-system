import mysql.connector
import os
from dotenv import load_dotenv

# تحميل المتغيرات من .env أو من Environment Variables في Render
load_dotenv()

def grant_access():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )

        cursor = connection.cursor()

        # أمر SQL للسماح بالاتصال من أي IP
        cursor.execute(f"""
            GRANT ALL PRIVILEGES ON *.* TO '{os.getenv("DB_USER")}'@'%' IDENTIFIED BY '{os.getenv("DB_PASSWORD")}';
        """)
        cursor.execute("FLUSH PRIVILEGES;")

        connection.commit()
        st.success("✅ تم السماح بالاتصال من أي IP بنجاح.")

    except Exception as e:
        st.error(f"❌ حصل خطأ: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Streamlit UI
import streamlit as st

st.title("Grant MySQL Remote Access")

if st.button("Grant Access"):
    grant_access()
