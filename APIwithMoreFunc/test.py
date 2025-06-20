# test_db_connection.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        dbname=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("password")
    )
    cursor = connection.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("✅ Connected! Time:", result)

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Connection failed:", e)
