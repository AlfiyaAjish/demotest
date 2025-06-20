from bson import ObjectId

def serialize_document(doc):
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

def serialize_documents(docs):
    return [serialize_document(doc) for doc in docs]
