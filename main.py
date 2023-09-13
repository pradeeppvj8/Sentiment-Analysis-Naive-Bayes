from sanbproject.logger import logging
from sanbproject.exception import CustomException
import sys

try:
    a = 2 / 0
except Exception as e:
    logging.info(e)
    raise CustomException(e, sys)