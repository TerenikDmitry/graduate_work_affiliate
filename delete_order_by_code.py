import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB
from base import get_info_logger

logger = get_info_logger('delete_order_by_code', 'delete')

mongo_db = MongoDB()
postgres_db = PostgresDB()


def delete_order_by_code():
    parser = argparse.ArgumentParser()
    parser.add_argument("order_code", help="Order code")
    args = parser.parse_args()
    order_code = args.order_code

    logger.info(f'START with args: order_code={order_code}')

    duration_time = mongo_db.delete_order_by_code(order_code)
    logger.info(f"[Mongo] delete order: {duration_time.total_seconds()}")

    duration_time = postgres_db.delete_order_by_code(order_code)
    logger.info(f"[Postgres] delete order: {duration_time.total_seconds()}")


if __name__ == "__main__":
    delete_order_by_code()
