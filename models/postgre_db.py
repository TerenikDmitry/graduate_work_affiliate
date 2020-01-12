import datetime

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

    def create_sql(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

    def insert_sql(self, sql, data):
        start_time = datetime.datetime.now()
        cur = self.con.cursor()
        cur.execute(sql, data)
        inserted_id = cur.fetchone()[0]
        self.con.commit()
        duration_time = datetime.datetime.now() - start_time
        return inserted_id, duration_time

    def select_sql(self, sql):
        start_time = datetime.datetime.now()
        cur = self.con.cursor()
        cur.execute(sql)
        duration_time = datetime.datetime.now() - start_time
        return cur.fetchall(), duration_time

    def create_user_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS "user"  
            (id SERIAL PRIMARY KEY,
            email varchar(256) unique,
            password_hash varchar(256),
            user_name varchar(256),
            active boolean default true);
        '''

        self.create_sql(sql)

    def create_coupon_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS "coupon"  
            (id SERIAL PRIMARY KEY,
            user_id integer REFERENCES "user" (id),
            code varchar(256) unique,
            percentage smallint);
        '''

        self.create_sql(sql)

    def create_order_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS "order"  
            (id SERIAL PRIMARY KEY,
            coupon_id integer REFERENCES "coupon" (id),
            code varchar(256) unique,
            product_code varchar(256),
            price numeric,
            created timestamp);
        '''

        self.create_sql(sql)

    def insert_user(self, user):
        sql = """
            INSERT INTO "user" 
            (email, password_hash, user_name, active) 
            VALUES 
            (%s, %s, %s, %s) 
            RETURNING "user".id;
        """
        user_data = (user.email, user.password_hash, user.user_name, user.active)

        return self.insert_sql(sql, user_data)

    def insert_coupon(self, user_id, user_coupon):
        sql = """
            INSERT INTO "coupon" 
            (user_id, code, percentage) 
            VALUES 
            (%s, %s, %s) 
            RETURNING "coupon".id;
        """
        coupon_data = (user_id, user_coupon[0], user_coupon[1])

        return self.insert_sql(sql, coupon_data)

    def insert_order(self, coupon_id, order):
        sql = """
            INSERT INTO "order" 
            (coupon_id, code, product_code, price, created) 
            VALUES 
            (%s, %s, %s, %s, %s) 
            RETURNING "order".id;
        """
        order_data = (coupon_id, order.order_code, order.product_code, order.price, order.date)

        return self.insert_sql(sql, order_data)

    def top_bestsellers(self, top_limit):
        sql = f'''
            SELECT u.user_name, sum("order".price)
            FROM "order"
                LEFT OUTER JOIN coupon c on "order".coupon_id = c.id
                LEFT JOIN "user" u on c.user_id = u.id
            GROUP BY u.id
            ORDER BY sum("order".price) DESC
            LIMIT {top_limit};
        '''
        return self.select_sql(sql)

    def orders_by_coupon(self, coupon_code):
        sql = f'''
            SELECT "order".code, "order".price
            FROM "order"
                LEFT OUTER JOIN coupon c on "order".coupon_id = c.id
            WHERE c.code = '{coupon_code}';
        '''
        return self.select_sql(sql)
