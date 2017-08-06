"""this file contains settings
- the directories for the output can be set
- it can be decided whether unknown values
for certain status fields, that might serve
as facets in the future should be reported
- the log level can be adjusted
"""
import os
import sys
import logging

# this is the base dir for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# this is the directory for the batchfile output
JSON_DIR = os.path.join(BASE_DIR, 'json')

# if set to true unknown values for status fields, that
# respresented in nyt_constants will be logged as warnings
NYT_REPORT_UNKNOWN_VALUES = False

# the logger is adjusted and the log level is set
log = logging.getLogger('NYTimes')
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
