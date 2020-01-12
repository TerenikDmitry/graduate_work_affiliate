import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

mongo_db = MongoDB()
postgres_db = PostgresDB()


def top_bestsellers():
    parser = argparse.ArgumentParser()
    parser.add_argument("top_limit",
                        help="Record limit",
                        type=int)
    args = parser.parse_args()
    top_limit = args.top_limit

    users, duration_time = mongo_db.top_bestsellers(top_limit)
    print(f"[Mongo] top bestsellers: {duration_time.total_seconds()}")
    for user in users:
        print(user)

    print("-"*10)

    users, duration_time = postgres_db.top_bestsellers(top_limit)
    print(f"[Postgres] top bestsellers: {duration_time.total_seconds()}")
    for user in users:
        print(user)


if __name__ == "__main__":
    top_bestsellers()
