import logging
def setup_logger() -> logging.Logger:
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)


    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)


    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

 
    logger.addHandler(ch)

    return logger