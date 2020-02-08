import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB
from base import get_info_logger

logger = get_info_logger('update_coupon_percentage', 'update')

mongo_db = MongoDB()
postgres_db = PostgresDB()


def set_coupon_percentage():
    parser = argparse.ArgumentParser()
    parser.add_argument("coupon_code",
                        help="Coupon code")
    parser.add_argument("percentage",
                        help="Coupon percentage",
                        type=float)
    args = parser.parse_args()
    coupon_code = args.coupon_code
    percentage = args.percentage

    logger.info(f'START with args: coupon_code={coupon_code}, percentage={percentage}')

    duration_time = mongo_db.set_coupon_percentage(coupon_code, percentage)
    logger.info(f"[Mongo] set coupon percentage: {duration_time.total_seconds()}")

    duration_time = postgres_db.set_coupon_percentage(coupon_code, percentage)
    logger.info(f"[Postgres] set coupon percentage: {duration_time.total_seconds()}")


if __name__ == "__main__":
    set_coupon_percentage()
