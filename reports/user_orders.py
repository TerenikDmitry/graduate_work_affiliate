from models.mongo_db import MongoDB

mongo_db_connection = MongoDB()
users = mongo_db_connection.get_users()
for user in users:
    print(user['user_name'])
    print(*[f"{order['order_code']}: "
            f"{order['coupon_percentage']}%: "
            f"{order['price']:.2f} USD: "
            f"{order['price']*order['coupon_percentage']/100:.2f} USD"
            for order in mongo_db_connection.get_user_orders(user_id=user['user_id'])],
          sep="\n")
