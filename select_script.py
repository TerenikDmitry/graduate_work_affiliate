from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

mongo_db = MongoDB()
postgres_db = PostgresDB()


def user_top_bestsellers(top_limit):
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
    user_top_bestsellers(top_limit=10)
