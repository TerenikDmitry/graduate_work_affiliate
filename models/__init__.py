from collections import namedtuple
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
mongo_host = config['mongo']['host']
mongo_port = config['mongo']['port']

User = namedtuple("User", [
    'user_id',
    'email',
    'password_hash',
    'user_name',
    'active'
])

Coupon = namedtuple("Coupon", [
    'user_id',
    'code',
    'percentage'
])
