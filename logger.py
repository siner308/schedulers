import logging


def get_my_logger(key):
    logger = logging.getLogger("%s" % key)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('/var/log/%s.log' % key)
    logger.addHandler(file_handler)

    return logger
