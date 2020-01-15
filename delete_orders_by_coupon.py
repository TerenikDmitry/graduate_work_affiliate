import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

mongo_db = MongoDB()
postgres_db = PostgresDB()


def delete_orders_by_coupon():
    parser = argparse.ArgumentParser()
    parser.add_argument("coupon_code",
                        help="Coupon code")
    args = parser.parse_args()
    coupon_code = args.coupon_code

    duration_time = mongo_db.delete_orders_by_coupon(coupon_code)
    print(f"[Mongo] delete orders: {duration_time.total_seconds()}")

    print("-"*10)

    duration_time = postgres_db.delete_orders_by_coupon(coupon_code)
    print(f"[Postgres] delete orders: {duration_time.total_seconds()}")


if __name__ == "__main__":
    delete_orders_by_coupon()
