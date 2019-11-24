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
        sql = '''
            CREATE TABLE IF NOT EXISTS "user"  
            (id SERIAL PRIMARY KEY,
            email varchar(256) unique,
            password_hash varchar(256),
            user_name varchar(256),
            active boolean default true);
        '''

        self.execute_sql(sql)

    def create_coupon_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS "coupon"  
            (id SERIAL PRIMARY KEY,
            user_id integer REFERENCES "user" (id),
            code varchar(256) unique,
            percentage smallint);
        '''

        self.execute_sql(sql)

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

        cur = self.con.cursor()
        cur.execute(sql, user_data)
        inserted_id = cur.fetchone()[0]
        self.con.commit()

        return inserted_id

    def insert_coupon(self, user_id, user_coupon):
        sql = """
            INSERT INTO "coupon" 
            (user_id, code, percentage) 
            VALUES 
            (%s, %s, %s) 
            RETURNING "coupon".id;
        """
        coupon_data = (user_id, user_coupon[0], user_coupon[1])

        cur = self.con.cursor()
        cur.execute(sql, coupon_data)
        inserted_id = cur.fetchone()[0]
        self.con.commit()

        return inserted_id

    def insert_order(self, coupon_id, order):
        sql = """
            INSERT INTO "order" 
            (coupon_id, code, product_code, price, created) 
            VALUES 
            (%s, %s, %s, %s, %s) 
            RETURNING "order".id;
        """
        order_data = (coupon_id, order.order_code, order.product_code, order.price, order.date)

        cur = self.con.cursor()
        cur.execute(sql, order_data)
        inserted_id = cur.fetchone()[0]
        self.con.commit()

        return inserted_id
