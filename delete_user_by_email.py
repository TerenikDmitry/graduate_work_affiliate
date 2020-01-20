import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('delete_user_by_email')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/delete.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def delete_user_by_email():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_email",
                        help="User email")
    args = parser.parse_args()
    user_email = args.user_email

    logger.info(f'START with args: user_email={user_email}')

    duration_time = mongo_db.delete_user_by_email(user_email)
    logger.info(f"[Mongo] delete user: {duration_time.total_seconds()}")

    duration_time = postgres_db.delete_user_by_email(user_email)
    logger.info(f"[Postgres] delete user: {duration_time.total_seconds()}")


if __name__ == "__main__":
    delete_user_by_email()
