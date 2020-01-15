import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

mongo_db = MongoDB()
postgres_db = PostgresDB()


def set_order_price():
    parser = argparse.ArgumentParser()
    parser.add_argument("order_code",
                        help="Product code")
    parser.add_argument("price",
                        help="Price",
                        type=float)
    args = parser.parse_args()
    order_code = args.order_code
    price = args.price

    duration_time = mongo_db.set_order_price(order_code, price)
    print(f"[Mongo] set order price: {duration_time.total_seconds()}")

    print("-"*10)

    duration_time = postgres_db.set_order_price(order_code, price)
    print(f"[Postgres] set order price: {duration_time.total_seconds()}")


if __name__ == "__main__":
    set_order_price()
