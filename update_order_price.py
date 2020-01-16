import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('set_order_price')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/update.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def set_order_price():
    parser = argparse.ArgumentParser()
    parser.add_argument("order_code",
                        help="Order code")
    parser.add_argument("price",
                        help="Order price",
                        type=float)
    args = parser.parse_args()
    order_code = args.order_code
    price = args.price

    logger.info(f'START with args: order_code={order_code}, price={price}')

    duration_time = mongo_db.set_order_price(order_code, price)
    logging.info(f"[Mongo] set order price: {duration_time.total_seconds()}")

    duration_time = postgres_db.set_order_price(order_code, price)
    logging.info(f"[Postgres] set order price: {duration_time.total_seconds()}")


if __name__ == "__main__":
    set_order_price()
