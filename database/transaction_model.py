# for pip: pip install bson
# for uv: uv add bson

from database.database_manager import DatabaseManager
import config
from datetime import datetime, date
from typing import Union
from bson.objectid import ObjectId

collection_name = config.COLLECTIONS['transaction']

class TransactionModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)

    def add_new_transaction(self, 
                            transaction_type: str,
                            category: str,
                            amount: float,
                            transaction_date: datetime | str  = None,
                            description: str = None ):
        
        # 1. Check datetime:
        # if transaction_date is only contain date and transaction_date is not datetime instance
        # at timestamp to it
        if isinstance(transaction_date, date) and not isinstance(transaction_date, datetime):
            transaction_date = datetime.combine(transaction_date, datetime.min.time())

        # 2. Create transaction object
        transaction_data = {
            "user_id": "default_user",
            "type": transaction_type,
            "category": category,
            "amount": float(amount),
            "transaction_date": transaction_date,
            "description": description,
            "created_at": datetime.now(),
            "last_modified": datetime.now()
        }

        # 3. insert into db
        result = self.collection.insert_one(transaction_data)
        return result.inserted_id
    
    def delete_transaction(self, 
                           transaction_id: Union[str, ObjectId]):
        result = self.collection.delete_one({"_id": ObjectId(transaction_id)})
        return result.deleted_count

    def get_all_transactions(self):
        pass