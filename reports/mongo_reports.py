from models.mongo_db import MongoDB


class MongoReport:
    def __init__(self):
        self.db_connection = MongoDB()

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
        return list(self.db_connection.user_collection.aggregate(pipeline))
