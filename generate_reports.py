from reports.mongo_reports import MongoReport
from reports.postgres_reports import PostgresReport

mongo_report = MongoReport()
postgres_report = PostgresReport()


def user_top_bestsellers(top_limit):
    users = mongo_report.top_bestsellers(top_limit)
    for user in users:
        print(user)
    print("-"*10)
    users = postgres_report.top_bestsellers(top_limit)
    for user in users:
        print(user)


if __name__ == "__main__":
    user_top_bestsellers(10)
