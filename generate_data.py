import random
import uuid
from datetime import datetime, timedelta
import hashlib
from collections import namedtuple

import names

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

User = namedtuple("User", [
    'user_id',
    'email',
    'password_hash',
    'user_name',
    'active'
])

AffiliateOrder = namedtuple("AffiliateOrder", [
    'user_id',
    'order_code',
    'product_code',
    'coupon_code',
    'coupon_percentage',
    'date',
    'price'
])


def generate_user_data(limit):
    mongo_db = MongoDB()
    postgres_db = PostgresDB()
    postgres_db.create_user_table()
    postgres_db.create_coupon_table()
    postgres_db.create_order_table()

    products = generate_products(50000)

    for _ in range(limit):
        user_id = get_random_code()
        user_name = names.get_full_name()
        email = get_user_email(user_name)
        password_hash = hashlib.sha224(get_random_code().encode('utf-8')).hexdigest()
        active = get_random_active()

        user = User(
            user_id=user_id,
            email=email,
            user_name=user_name,
            password_hash=password_hash,
            active=active
        )
        mongo_db.insert_user(user)
        user_id = postgres_db.insert_user(user)

        user_coupons = generate_user_coupons(1, 10)
        for user_coupon in user_coupons:
            coupon_id = postgres_db.insert_coupon(user_id, user_coupon)
            number_of_orders = random.randint(a=10, b=100)
            for _ in range(number_of_orders):
                order = generate_order(user, user_coupon, random.choice(products))
                mongo_db.insert_order(order)
                order_id = postgres_db.insert_order(coupon_id, order)


def generate_order(user, coupon, product):
    order_code = get_random_code()
    order_date = get_random_date()
    return AffiliateOrder(
        product_code=product[0],
        date=order_date,
        price=product[1],
        user_id=user.user_id,
        order_code=order_code,
        coupon_percentage=coupon[1],
        coupon_code=coupon[0],
    )


def generate_user_coupons(min_limit, max_limit):
    return [tuple([get_random_code(), get_random_percentage(1, 50)]) for _ in range(random.randint(a=min_limit, b=max_limit))]


def generate_products(limit):
    return [tuple([get_random_code(), get_random_price(10, 1000)]) for _ in range(limit)]


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
    generate_user_data(5000)
