import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('orders_by_coupon')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/select.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def orders_by_coupon():
    parser = argparse.ArgumentParser()
    parser.add_argument("coupon_code",
                        help="Coupon code")
    args = parser.parse_args()
    coupon_code = args.coupon_code

    logger.info(f'START with args: coupon_code={coupon_code}')

    orders, duration_time = mongo_db.orders_by_coupon(coupon_code)
    logger.info(f"[Mongo] orders by coupon: {duration_time.total_seconds()}")
    for order in orders:
        logger.info(f"order: {order}")

    orders, duration_time = postgres_db.orders_by_coupon(coupon_code)
    logger.info(f"[Postgres] orders by coupon: {duration_time.total_seconds()}")
    for order in orders:
        logger.info(f"order: {order}")


if __name__ == "__main__":
    orders_by_coupon()
