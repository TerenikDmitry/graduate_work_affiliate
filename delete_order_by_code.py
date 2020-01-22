import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('delete_order_by_code')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/delete.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def delete_order_by_code():
    parser = argparse.ArgumentParser()
    parser.add_argument("order_code",
                        help="Order code")
    args = parser.parse_args()
    order_code = args.order_code

    logger.info(f'START with args: order_code={order_code}')

    duration_time = mongo_db.delete_order_by_code(order_code)
    logger.info(f"[Mongo] delete order: {duration_time.total_seconds()}")

    duration_time = postgres_db.delete_order_by_code(order_code)
    logger.info(f"[Postgres] delete order: {duration_time.total_seconds()}")


if __name__ == "__main__":
    delete_order_by_code()
