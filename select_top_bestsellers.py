import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('top_bestsellers')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/select.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def top_bestsellers():
    parser = argparse.ArgumentParser()
    parser.add_argument("top_limit",
                        help="Record limit",
                        type=int)
    args = parser.parse_args()
    top_limit = args.top_limit

    logger.info(f'START with args: top_limit={top_limit}')

    users, duration_time = mongo_db.top_bestsellers(top_limit)
    logging.info(f"[Mongo] top bestsellers: {duration_time.total_seconds()}")
    for user in users:
        logging.info(f"user: {user}")

    users, duration_time = postgres_db.top_bestsellers(top_limit)
    logging.info(f"[Postgres] top bestsellers: {duration_time.total_seconds()}")
    for user in users:
        logging.info(f"user: {user}")


if __name__ == "__main__":
    top_bestsellers()
