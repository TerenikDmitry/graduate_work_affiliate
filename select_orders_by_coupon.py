import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

mongo_db = MongoDB()
postgres_db = PostgresDB()


def orders_by_coupon():
    parser = argparse.ArgumentParser()
    parser.add_argument("coupon_code",
                        help="Coupon code")
    args = parser.parse_args()
    coupon_code = args.coupon_code

    orders, duration_time = mongo_db.orders_by_coupon(coupon_code)
    print(f"[Mongo] orders by coupon: {duration_time.total_seconds()}")
    for order in orders:
        print(order)

    print("-"*10)

    orders, duration_time = postgres_db.orders_by_coupon(coupon_code)
    print(f"[Postgres] orders by coupon: {duration_time.total_seconds()}")
    for order in orders:
        print(order)


if __name__ == "__main__":
    orders_by_coupon()
