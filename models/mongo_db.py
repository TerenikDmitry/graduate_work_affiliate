from pymongo import MongoClient

from models import (
    mongo_host,
    mongo_port,
)


class MongoDB:
    def __init__(self):
        client = MongoClient(mongo_host, int(mongo_port))

        self.affiliate_db = client['affiliate_db']
        self.user_collection = self.affiliate_db['users']
        self.order_collection = self.affiliate_db['orders']

    def insert_user(self, user, orders):
        user_data = user._asdict()
        user_data['orders'] = orders
        result = self.user_collection.insert_one(user_data)
        return result.inserted_id
