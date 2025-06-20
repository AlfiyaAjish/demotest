import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from scripts.constants.app_constants import ERROR_MESSAGES

load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        raise ConnectionError(f"{ERROR_MESSAGES['database_connection_failed']}: {str(e)}")

def run_query(query: str, params: tuple = ()):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        if cursor.description:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
        return result
    except Exception as e:
        raise RuntimeError(f"{ERROR_MESSAGES['query_execution_failed']}: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
