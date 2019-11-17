import psycopg2

from models import (
    postgres_database,
    postgres_user,
    postgres_password,
    postgres_host,
    postgres_port,
)


class PostgresDB:
    def __init__(self):
        self.con = psycopg2.connect(
            database=postgres_database,
            user=postgres_user,
            password=postgres_password,
            host=postgres_host,
            port=postgres_port
        )
