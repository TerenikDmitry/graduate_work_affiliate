import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('user_coupons')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/select.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def user_coupons():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_email",
                        help="User email")
    args = parser.parse_args()
    user_email = args.user_email

    logger.info(f'START with args: user_email={user_email}')

    coupons, duration_time = mongo_db.user_coupons(user_email)
    logging.info(f"[Mongo] user coupons: {duration_time.total_seconds()}")
    for coupon in coupons:
        logging.info(f"coupon: {coupon}")

    coupons, duration_time = postgres_db.user_coupons(user_email)
    logging.info(f"[Postgres] user coupons: {duration_time.total_seconds()}")
    for coupon in coupons:
        logging.info(f"coupon: {coupon}")


if __name__ == "__main__":
    user_coupons()
