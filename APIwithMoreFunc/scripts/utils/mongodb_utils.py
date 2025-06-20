from pymongo import MongoClient
from dotenv import load_dotenv
import os
from scripts.constants.app_constants import ERROR_MESSAGES

load_dotenv()

def get_mongo_collection(table_name):
    try:
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB")
        collection_name = table_name

        client = MongoClient(uri)
        db = client[db_name]
        return db[collection_name]
    except Exception as e:
        raise ConnectionError(f"{ERROR_MESSAGES['database_connection_failed']}: {str(e)}")
