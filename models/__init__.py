from collections import namedtuple
import random
import uuid
from datetime import datetime, timedelta
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


def get_random_date():
    # 260 weeks ~ 5 years
    end = datetime.now()
    start = end - timedelta(weeks=260)
    return start + (end - start) * random.random()


def get_random_percentage():
    return random.randint(a=1, b=50)


def get_random_code():
    return str(uuid.uuid1())


def get_random_price():
    return random.uniform(a=1, b=300)
