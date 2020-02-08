import logging

logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_info_logger(logger_name, file_name):
    logger = logging.getLogger(logger_name)

    ch = logging.FileHandler(filename=f'logs/{file_name}.log')
    ch.setLevel(logging.INFO)
    ch.setFormatter(logger_formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(ch)

    return logger
