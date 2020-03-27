import logging


def run(ds, **kwargs):
    logging.info('-------------------')
    logging.info(ds)
    logging.info('-------------------')
    logging.info(kwargs)
    logging.info('-------------------')
    logging.info('Hello World!')
    return True
