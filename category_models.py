from database_manager import DatabaseManager
import config
from datetime import datetime

collection_name = config.COLLECTIONS['category']

class CategoryModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.collection = self.db_manager.get_collection(collection_name=collection_name)
        self._initialize_default_categories()

    def _initialize_default_categories(self):
        """Initialize categories if they dont exist"""
        # EXPENSE
        for cate in config.DEFAULT_CATEGORIES_EXPENSE:
            item = {
                "type": "Expense",
                "name": cate,
                "created_at": datetime.now(),
                "last_modified": datetime.now()
            }
            self.collection.update_one(
                {"name": cate, "type": "Expense"},
                {"$setOnInsert": item},
                upsert=True
            )
            print(f"Initialize {cate} success, type Expense!!")

        # INCOME
        for cate in config.DEFAULT_CATEGORIES_INCOME:
            item = {
                "type": "Income",
                "name": cate,
                "created_at": datetime.now(),
                "last_modified": datetime.now()
            }
            self.collection.update_one(
                {"name": cate, "type": "Expense"},
                {"$setOnInsert": item},
                upsert=True
            )

    def add_category(self, type: str, category_name: str):
        item_add = {
            "type": type,
            "name": category_name,
            "created_at": datetime.now()
        }
        try:
            result = self.collection.insert_one(item_add)
            return result.inserted_id
        except Exception as e:
            print(f"Error {e}")
            return None

    def delete_category(self, type: str, category_name: str):
        result = self.collection.delete_one({"type": type, "name": category_name})
        return result

    def get_category_by_type(self, type: str):
        result = self.collection.find({"type": type})
        result = list(result)
        return result
    
    def get_total(self):
        result = self.collection.find({})
        result = list(result)
        return result

# if __name__ == "__main__":
#     print("Init cate collection")
#     cate = CategoryModel()

#     item = {
#         "type": "Expense",
#         "name": "Rent"
#     }

#     result = cate.add_category(type = "Expense", category_name="Rent")