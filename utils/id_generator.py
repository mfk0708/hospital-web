from database import counter_collections
from pymongo import ReturnDocument

def get_next_sequence(prefix: str) -> str:
    result = counter_collections.find_one_and_update(
        {"_id": prefix},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return f"{prefix}{result['sequence_value']}"
