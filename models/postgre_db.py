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

    def execute_sql(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

    def create_user_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "user"  
                 (id integer PRIMARY KEY NOT NULL,
                 email varchar(256) unique,
                 password_hash varchar(256),
                 user_name varchar(256),
                 active boolean default true);'''

        self.execute_sql(sql)

    def create_coupon_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "coupon"  
                 (id INT PRIMARY KEY NOT NULL,
                 user_id integer unique REFERENCES "user" (id),
                 code varchar(256) unique,
                 percentage smallint);'''

        self.execute_sql(sql)

    def create_order_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS "order"  
                 (id INT PRIMARY KEY NOT NULL,
                 coupon_id integer unique REFERENCES "coupon" (id),
                 code varchar(256) unique,
                 product_code varchar(256),
                 price numeric,
                 created timestamp);'''

        self.execute_sql(sql)
