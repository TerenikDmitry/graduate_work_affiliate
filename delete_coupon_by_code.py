import argparse

from models.mongo_db import MongoDB
from models.postgres_db import PostgresDB
from base import get_info_logger

logger = get_info_logger('delete_coupon_by_code', 'delete')

mongo_db = MongoDB()
postgres_db = PostgresDB()


def delete_coupon_by_code():
    parser = argparse.ArgumentParser()
    parser.add_argument("coupon_code", help="Coupon code")
    args = parser.parse_args()
    coupon_code = args.coupon_code

    logger.info(f'START with args: coupon_code={coupon_code}')

    duration_time = mongo_db.delete_coupon_by_code(coupon_code)
    logger.info(f"[Mongo] delete coupon: {duration_time.total_seconds()}")

    duration_time = postgres_db.delete_coupon_by_code(coupon_code)
    logger.info(f"[Postgres] delete coupon: {duration_time.total_seconds()}")


if __name__ == "__main__":
    delete_coupon_by_code()
