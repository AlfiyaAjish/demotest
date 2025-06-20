import pandas as pd
from scripts.utils.mongodb_utils  import get_mongo_collection

def upload_to_mongo(df: pd.DataFrame, collection_name: str, create_new: bool):
    collection = get_mongo_collection(collection_name)

    if create_new:
        collection.drop()

    collection.insert_many(df.to_dict(orient="records"))
