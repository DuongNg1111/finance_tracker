# for pip: pip install bson
# for uv: uv add bson

from database.database_manager import DatabaseManager
import config
from datetime import datetime, date
from typing import Union, Any, Optional
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
    
    def get_transaction_by_id(self, transaction_id: Union[str, ObjectId]):
        try:
            result = self.collection.find_one({"_id": ObjectId(transaction_id)})
            return result
        except Exception as e:
            print(f"Failed to retrieve transaction: {transaction_id}, error {e}")
            return

    def get_all_transactions(self,
                            filters: dict[str, Any] = None):
        query_ = self._build_filter_query(filters)

        cursor = self.collection.find(query_).sort("created_at", -1)
        return list(cursor)

    def _build_filter_query(self, filters: dict[str, Any]) -> dict:
        query = {}

        # Check transaction_type:
        if "transaction_type" in filters:
            query["type"] = filters.get("transaction_type")

        # Check Category:
        if "category" in filters:
            query["category"] = filters.get("category")

        # Check amount:
        min_amount = filters.get("min_amount")
        max_amount = filters.get("max_amount")
        if min_amount or max_amount:
            query['amount'] = {}
            if min_amount is not None:
                query['amount']["$gte"] = min_amount # $gte = greater than or equal
            if max_amount is not None:
                query['amount']["$lte"] = max_amount # $lte = less than or equal

        # Check datetime
        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        if start_date or end_date:
            query['transaction_date'] = {}
            if start_date is not None:
                query['transaction_date']["$gte"] = start_date # $gte = greater than or equal
            if end_date is not None:
                query['transaction_date']["$lte"] = end_date # $lte = less than or equal

        # Check description:
        if "search_text" in filters:
            query['description'] = {
                "$regex": filters.get("search_text"),
                "$option": "i"
            }

        return query