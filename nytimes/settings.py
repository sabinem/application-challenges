"""this file contains settings
- the directory for the json output is specified
- the log leve is set
"""
import os
import sys
import logging

# constants for Directory Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, 'json')

NYT_REPORT_UNKNOWN_VALUES = False

log = logging.getLogger('NYTimes')
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
