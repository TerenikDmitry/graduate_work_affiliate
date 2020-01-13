import argparse

from models.mongo_db import MongoDB
from models.postgre_db import PostgresDB

mongo_db = MongoDB()
postgres_db = PostgresDB()


def user_coupons():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_email",
                        help="User email")
    args = parser.parse_args()
    user_email = args.user_email

    coupons, duration_time = mongo_db.user_coupons(user_email)
    print(f"[Mongo] user coupons: {duration_time.total_seconds()}")
    for coupon in coupons:
        print(coupon)

    print("-"*10)

    coupons, duration_time = postgres_db.user_coupons(user_email)
    print(f"[Postgres] user coupons: {duration_time.total_seconds()}")
    for coupon in coupons:
        print(coupon)


if __name__ == "__main__":
    user_coupons()
