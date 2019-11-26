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

    def insert_user(self, user):
        user_data = user._asdict()
        result = self.user_collection.insert_one(user_data)
        return result.inserted_id

    def insert_order(self, user_id, order):
        order_data = order._asdict()
        order_data['user_id'] = user_id
        result = self.order_collection.insert_one(order._asdict())
        return result.inserted_id

    def get_users(self, active=None):
        filters = {'active': active} if active else {}
        users = self.user_collection.find(filters)
        return users

    def get_user_orders(self, user_id):
        filters = {'user_id': user_id}
        users = self.order_collection.find(filters)
        return users
