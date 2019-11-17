import configparser


config = configparser.ConfigParser()
config.read('config.ini')
mongo_host = config['mongo']['host']
mongo_port = config['mongo']['port']

postgres_database = config['postgres']['database']
postgres_user = config['postgres']['user']
postgres_password = config['postgres']['password']
postgres_host = config['postgres']['host']
postgres_port = config['postgres']['port']
