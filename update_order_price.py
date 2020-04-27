import argparse

from models.mongo_db import MongoDB
from models.postgres_db import PostgresDB
from base import get_info_logger

logger = get_info_logger('update_order_price', 'update')

mongo_db = MongoDB()
postgres_db = PostgresDB()


def set_order_price():
    parser = argparse.ArgumentParser()
    parser.add_argument("order_code", help="Order code")
    parser.add_argument("price", help="Order price", type=float)
    args = parser.parse_args()
    order_code = args.order_code
    price = args.price

    logger.info(f'START with args: order_code={order_code}, price={price}')

    duration_time = mongo_db.set_order_price(order_code, price)
    logger.info(f"[Mongo] set order price: {duration_time.total_seconds()}")

    duration_time = postgres_db.set_order_price(order_code, price)
    logger.info(f"[Postgres] set order price: {duration_time.total_seconds()}")


if __name__ == "__main__":
    set_order_price()
