# encoding: utf-8
import csv
import os
import logging
def setup_logging():
    """Set up logging configuration."""
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(
        filename='log/agent.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        encoding='utf-8-sig'
    )
    logger = logging.getLogger('gemini data handler')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('log/agent.log', encoding='utf-8-sig')
    logger.addHandler(handler)
    return logger
logger = setup_logging()