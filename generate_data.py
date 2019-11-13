import json
import hashlib
from random import randint

from models import (
    User,
    get_random_code,
    get_random_percentage,
    get_random_date,
    get_random_price,
)
from models.mongo_db import MongoDB, AffiliateOrder


def load_user_data():
    mongo_db_connection = MongoDB()

    with open('static/user_data.json') as json_file:
        #
        # Example of file
        # [
        # ...
        #   {
        #       "user_id": "5db5c537191920a05b652903",
        #       "email": "loriebullock@terrasys.com",
        #       "password": "91bd7d4b-59e9-4778-a5b5-6055e8fe4d26",
        #       "user_name": "Eva Goff",
        #       "active": true
        #   },
        # ...
        # ]

        data = json.load(json_file)
        for row in data:
            user = User(
                user_id=row['user_id'],
                email=row['email'],
                user_name=row['user_name'],
                password_hash=hashlib.sha224(row['password'].encode('utf-8')).hexdigest(),
                active=row['active']
            )
            mongo_db_connection.insert_user(user)

            for _ in range(randint(a=0, b=5)):
                order_code = get_random_code()
                product_code = get_random_code()
                coupon_code = get_random_code()
                percentage = get_random_percentage()
                date = get_random_date()
                price = get_random_price()
                affiliate_order = AffiliateOrder(
                    order_code=order_code,
                    product_code=product_code,
                    coupon_percentage=percentage,
                    coupon_code=coupon_code,
                    user_id=user.user_id,
                    date=date,
                    price=price,
                )
                mongo_db_connection.insert_order(affiliate_order)


if __name__ == "__main__":
    load_user_data()
