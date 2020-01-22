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

    def execute_sql(self, sql):
        start_time = datetime.datetime.now()

        cur = self.con.cursor()
        cur.execute(sql)
        self.con.commit()

        duration_time = datetime.datetime.now() - start_time
        return duration_time

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
            email VARCHAR(256) UNIQUE,
            password_hash VARCHAR(256),
            user_name VARCHAR(256),
            active boolean DEFAULT TRUE);
        '''
        self.execute_sql(sql)

    def create_coupon_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS "coupon"  
            (id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES "user" (id) ON DELETE CASCADE,
            code VARCHAR(256) UNIQUE,
            percentage SMALLINT);
        '''
        self.execute_sql(sql)

    def create_order_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS "order"  
            (id SERIAL PRIMARY KEY,
            coupon_id INTEGER REFERENCES "coupon" (id) ON DELETE CASCADE,
            code VARCHAR(256) UNIQUE,
            product_code VARCHAR(256),
            price NUMERIC,
            created TIMESTAMP);
        '''
        self.execute_sql(sql)

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
                LEFT OUTER JOIN coupon c ON "order".coupon_id=c.id
                LEFT JOIN "user" u ON c.user_id=u.id
            GROUP BY u.id
            ORDER BY sum("order".price) DESC
            LIMIT {top_limit};
        '''
        return self.select_sql(sql)

    def orders_by_coupon(self, coupon_code):
        sql = f'''
            SELECT "order".code, "order".price
            FROM "order"
                LEFT OUTER JOIN "coupon" c ON "order".coupon_id=c.id
            WHERE c.code = '{coupon_code}';
        '''
        return self.select_sql(sql)

    def user_coupons(self, user_email):
        sql = f'''
            SELECT "coupon".code, "coupon".percentage
            FROM "coupon"
                LEFT OUTER JOIN "user" u ON "coupon".user_id=u.id
            WHERE u.email = '{user_email}'
            ORDER BY "coupon".percentage DESC;
        '''
        return self.select_sql(sql)

    def set_order_price(self, order_code, price):
        sql = f'''
            UPDATE "order"
            SET price = {price}
            WHERE code = '{order_code}';
        '''
        return self.execute_sql(sql)

    def set_coupon_percentage(self, coupon_code, percentage):
        sql = f'''
            UPDATE "coupon"
            SET percentage = {percentage}
            WHERE code = '{coupon_code}';
        '''
        return self.execute_sql(sql)

    def delete_order_by_code(self, order_code):
        sql = f'''
            DELETE 
            FROM "order"
            WHERE code = '{order_code}';
        '''
        return self.execute_sql(sql)

    def delete_user_by_email(self, user_email):
        sql = f'''
            DELETE 
            FROM "user"
            WHERE email = '{user_email}';
        '''
        return self.execute_sql(sql)

    def delete_coupon_by_code(self, coupon_code):
        sql = f'''
            DELETE 
            FROM "coupon"
            WHERE code = '{coupon_code}';
        '''
        return self.execute_sql(sql)
