import argparse
import random
import uuid
from datetime import datetime, timedelta
import hashlib
from collections import namedtuple

import names

from models.mongo_db import MongoDB
from models.postgres_db import PostgresDB
from base import get_info_logger

logger = get_info_logger('generate_user_data', 'insert')

User = namedtuple("User", [
    'email',
    'password_hash',
    'user_name',
    'active'
])

AffiliateOrder = namedtuple("AffiliateOrder", [
    'order_code',
    'product_code',
    'coupon_code',
    'coupon_percentage',
    'date',
    'price'
])


def generate_user_data():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_count", type=int, help="User count")
    parser.add_argument("product_count", type=int, help="Product count")
    args = parser.parse_args()
    user_count = args.user_count
    product_count = args.product_count

    logger.info(f'START with args: user_count={user_count}, product_count={product_count}')

    mongo_db = MongoDB()
    postgres_db = PostgresDB()
    postgres_db.create_user_table()
    postgres_db.create_coupon_table()
    postgres_db.create_order_table()

    products = generate_products(product_count)

    duration_time_mongo = timedelta(0)
    duration_time_postgres = timedelta(0)
    for _ in range(user_count):
        user_name = names.get_full_name()
        email = get_user_email(user_name)
        password_hash = hashlib.sha224(get_random_code().encode('utf-8')).hexdigest()
        active = get_random_active()

        user = User(
            email=email,
            user_name=user_name,
            password_hash=password_hash,
            active=active
        )
        user_id_postgres, duration_time = postgres_db.insert_user(user)
        duration_time_postgres += duration_time

        user_coupons = generate_user_coupons(1, 10)
        user_orders = []
        for user_coupon in user_coupons:
            coupon_id_postgres, duration_time = postgres_db.insert_coupon(user_id_postgres, user_coupon)
            duration_time_postgres += duration_time

            orders_count = random.randint(a=10, b=100)
            for _ in range(orders_count):
                product = random.choice(products)
                order = AffiliateOrder(
                    product_code=product[0],
                    date=get_random_date(),
                    price=product[1],
                    order_code=get_random_code(),
                    coupon_percentage=user_coupon[1],
                    coupon_code=user_coupon[0],
                )
                user_orders.append(order._asdict())
                _, duration_time = postgres_db.insert_order(coupon_id_postgres, order)
                duration_time_postgres += duration_time

        _, duration_time = mongo_db.insert_user(user, user_orders)
        duration_time_mongo += duration_time

    logger.info(f"[Mongo]: {duration_time_mongo.total_seconds()}")
    logger.info(f"[Postgres]: {duration_time_postgres.total_seconds()}")


def generate_user_coupons(min_limit, max_limit):
    coupon_count = random.randint(a=min_limit, b=max_limit)
    return [(get_random_code(), get_random_percentage(1, 50))
            for _ in range(coupon_count)]


def generate_products(limit):
    return [(get_random_code(), get_random_price(10, 1000))
            for _ in range(limit)]


def get_random_date():
    # 260 weeks ~ 5 years
    end = datetime.now()
    start = end - timedelta(weeks=260)
    return start + (end - start) * random.random()


def get_random_percentage(min_percentage, max_percentage):
    return random.randint(a=min_percentage, b=max_percentage)


def get_random_code():
    return str(uuid.uuid1())


def get_random_price(min_price, max_price):
    return round(random.uniform(a=min_price, b=max_price), 2)


def get_random_active():
    return not not random.getrandbits(1)


def get_user_email(user_name):
    email_salt = random.randint(a=1, b=2000)
    return f"{user_name.lower().replace(' ', '_')}{email_salt}@mail.com"


if __name__ == "__main__":
    generate_user_data()
