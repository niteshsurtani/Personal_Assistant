import logging
from datetime import date
import time
import os.path

directory = "logs/"

# create logger
global logger
logger = logging.getLogger('nlp_preprocessing')
logger.setLevel(logging.DEBUG)

today = date.today()
todayString = today.isoformat()


if not os.path.isfile(directory + todayString):
	os.system("touch " + directory + todayString)

# create console handler and set level to debug
global loggingHandler
loggingHandler = logging.FileHandler(directory + todayString)
loggingHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s','%a, %d %b %Y %H:%M:%S')

# add formatter to ch
loggingHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(loggingHandler)
