import argparse
import logging

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

logger = logging.getLogger('set_user_active')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.FileHandler(filename='logs/update.log')
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)

mongo_db = MongoDB()
postgres_db = PostgresDB()


def set_user_active():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_email",
                        help="User email")
    parser.add_argument("active",
                        help="Active flag",
                        type=bool)
    args = parser.parse_args()
    user_email = args.user_email
    active = args.active

    logger.info(f'START with args: user_email={user_email}, active={active}')

    duration_time = mongo_db.set_user_active(user_email, active)
    logger.info(f"[Mongo] set user active: {duration_time.total_seconds()}")

    duration_time = postgres_db.set_user_active(user_email, active)
    logger.info(f"[Postgres] set user active: {duration_time.total_seconds()}")


if __name__ == "__main__":
    set_user_active()