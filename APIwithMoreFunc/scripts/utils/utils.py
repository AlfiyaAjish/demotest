# import psycopg2
#
# def get_postgres_conn():
#     return psycopg2.connect(
#         "postgresql://postgres:Alfiya%402821@db.mcouoyrvvfminhjwvqgl.supabase.co:5432/postgres"
#     )
#
#
from dotenv import load_dotenv
from scripts.constants.app_constants import ERROR_MESSAGES
import psycopg2
from psycopg2.extras import RealDictCursor
import os
load_dotenv()

def get_postgres_conn():
    try:
        connection = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        raise ConnectionError(f"{ERROR_MESSAGES['database_connection_failed']}: {str(e)}")