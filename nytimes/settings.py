"""
This file contains settings for the NY Times Articles Dataloader

- the directories for the output can be set

- it can be decided whether unknown values
for certain status fields should be reported

- the log level can be adjusted
"""
import os
import sys
import logging

# this is the base dir for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# this is the directory for the batchfile output
JSON_DIR = os.path.join(BASE_DIR, 'json')

# if set to true unknown values for certain fields, that
# are have discrete values will be logged as warnings
# see also nyt_constants.py
NYT_REPORT_UNKNOWN_VALUES = False

# the logger is adjusted and the log level is set
log = logging.getLogger('NYTimes')
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
