"""Access program for the NY Times Article Dataloader
- gives the dataloader a command line interface
- requests the batches from the dataloader
"""
import argparse
import datetime
import textwrap
from nytimes import nytimes


def valid_date(datearg):
    """checks whether arguments is a valid date"""
    try:
        datetime.datetime.strptime(datearg, "%Y%m%d")
    except (ValueError) as m:
        msg = "Not a valid date: '{0}'.".format(datearg)
        raise argparse.ArgumentTypeError(msg)
    else:
        return datearg


# define arguments
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
             ------------------------------------------------------
                        Dataloader for the New York Times API
             ------------------------------------------------------
                 To start the Dataloader use the parameters above.

                 - You need a valid API Key:
                 get it from

                 - Best start with a narrow date range!

                 - The result will be writen as JSON into a file,
                 with the query parameters as file name. You find it
                 in the 'json' directory

                 - The query can take some time, since the API allows
                 only to fetch 10 records at a time and the program
                 goes to sleep for some seconds between fetching data
                 in order to avoid the limit of too many requests
                 per second.

                 - You will see your progress, once you start the program!
             '''))
parser.add_argument("nr_batches",
                    help="number of batches that shall be fetched",
                    type=int)
parser.add_argument("api-key", help="your NY Times api-key",
                    type=str)
parser.add_argument("-b",
                    "--begin_date",
                    help="begin date as YYYYMMDD",
                    type=valid_date)
parser.add_argument("-e",
                    "--end_date",
                    help="end date as YYYYMMDD",
                    type=valid_date)
parser.add_argument("-q",
                    "--q",
                    help="queryterm for the article search",
                    type=str)

# parse the arguments and set configuration
args = parser.parse_args()
config = vars(args)

# pop args that are not set from the configuration
for k, v in config.items():
    if not v:
        config.pop(k)

# pop number of batches
nr_batches = config.pop('nr_batches')

# configure the source
source = nytimes.NYTimesSource(**config)

# request batches of articles
# only now will the source be accessed
try:
    for idx, batch in enumerate(source.getDataBatch(nr_batches)):
        print u'Received Batch {1} of {0} items'.format(len(batch), idx+1)
        for item in batch:
            print u'  - {0} - {1}'.format(item['_id'], item['headline.main'])
except (IOError) as e:
    print "ERROR: {}".format(e)
