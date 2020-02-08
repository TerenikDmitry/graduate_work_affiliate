import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB
from base import get_info_logger

logger = get_info_logger('user_coupons', 'select')

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
    logger.info(f"[Mongo] user coupons: {duration_time.total_seconds()}")
    for coupon in coupons:
        logger.info(f"coupon: {coupon}")

    coupons, duration_time = postgres_db.user_coupons(user_email)
    logger.info(f"[Postgres] user coupons: {duration_time.total_seconds()}")
    for coupon in coupons:
        logger.info(f"coupon: {coupon}")


if __name__ == "__main__":
    user_coupons()
