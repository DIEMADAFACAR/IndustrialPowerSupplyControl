import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')

file_handler = logging.FileHandler('telemetry.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


async def log_telemetry(data):
    log_message = f"{datetime.datetime.now()} - {data}"
    logger.info(log_message)
