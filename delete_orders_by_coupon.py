import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('delete_orders_by_coupon')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/delete.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def delete_orders_by_coupon():
    parser = argparse.ArgumentParser()
    parser.add_argument("coupon_code",
                        help="Coupon code")
    args = parser.parse_args()
    coupon_code = args.coupon_code

    logger.info(f'START with args: coupon_code={coupon_code}')

    duration_time = mongo_db.delete_orders_by_coupon(coupon_code)
    logger.info(f"[Mongo] delete orders: {duration_time.total_seconds()}")

    duration_time = postgres_db.delete_orders_by_coupon(coupon_code)
    logger.info(f"[Postgres] delete orders: {duration_time.total_seconds()}")


if __name__ == "__main__":
    delete_orders_by_coupon()
