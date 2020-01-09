import datetime

from pymongo import MongoClient

from models import (
    mongo_host,
    mongo_port,
)


class MongoDB:
    def __init__(self):
        self.client = MongoClient(mongo_host, int(mongo_port))

        affiliate_db = self.client['affiliate_db']
        self.user_collection = affiliate_db['users']

    def insert_user(self, user, orders):
        user_data = user._asdict()
        user_data['orders'] = orders

        start_time = datetime.datetime.now()
        result = self.user_collection.insert_one(user_data)
        duration_time = datetime.datetime.now() - start_time

        return result.inserted_id, duration_time

    def top_bestsellers(self, top_limit):
        pipeline = [
            {
                "$project": {
                    "user_name": "$user_name",
                    "orderTotal": { "$sum": "$orders.price"},
                }
            },
            {
                "$sort": { "orderTotal": -1 }
            },
            {
                "$limit": top_limit
            }
        ]

        start_time = datetime.datetime.now()
        result = self.user_collection.aggregate(pipeline)
        duration_time = datetime.datetime.now() - start_time

        return list(result), duration_time
