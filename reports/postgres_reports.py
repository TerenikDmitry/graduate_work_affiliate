from models.postgre_db import PostgresDB


class PostgresReport:
    def __init__(self):
        self.db_connection = PostgresDB()

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
        return self.db_connection.select_sql(sql)
