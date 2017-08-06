# -*- coding: utf-8 -*-
"""
Dataloader for NYTimes API

"""
import json
import urllib
import time
import os

import nyt_constants
import makeflat

from settings import log, JSON_DIR, NYT_REPORT_UNKNOWN_VALUES


def make_outputfile_name(query):
    """
    makes a filename from query dict
    """
    query_parms = [v.lower().replace(" ", "-") for k, v in query.items()]
    return '_'.join(query_parms)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API.
    - gets for one request

    the API brings back only 10 records at a time, but reports the
    total number of hits for the query.

    the records are then fetched in batches of 10 or less record and
    the program goes to sleep for 5 seconds between requests,
    to avoid the rate limit of the API

    the progress is reported to the user

    also unknown fields are logged

    the api seems to change frequently, so be aware
    of that!
    """
    def __init__(self, **config):
        """
        the configuration is completed by the api-key,
        that is here taken from constants but could also
        be an environmental variable

        the queryconfig is the confiq minus the api-key,
        which is supposed to be secret

        the outputfilename for the json data is derived
        from the queryconfig, so that different data are
        stored in different files

        the data is fetched in batches of 10 records each

        the initial connect to the source is special,
        since it brings back the meta data and also
        the file for writing the json data must be opened
        and overwriten, whereas subsequent request just add
        to that file
        """
        self.config = config

        self.queryconfig = config.copy()
        self.queryconfig.pop('api-key')

        log.info("configuration with api-key removed: {}"
                 .format(json.dumps(self.queryconfig,
                                    sort_keys=True,
                                    indent=4)))

        self.batches = []

        self.outputfilename = make_outputfile_name(self.queryconfig)

    def connect(self):
        """connect to url
        - get meta data (total hits)
        - get first batch of 10 articles
        - the program goes to sleep between API requests
        in order to avoid the rate limit
        """
        while not self.disconnect():

            # sleep between request to avoid API Rate limit
            time.sleep(5)
            log.debug("next api request: {}"
                      .format(json.dumps(self.config,
                                         sort_keys=True,
                                         indent=4)))
            try:
                # connect to API
                urlparams = urllib.urlencode(self.config)
                response = urllib.urlopen(
                    "https://api.nytimes.com/svc/search/v2/articlesearch.json?%s"
                    % urlparams)

            except IOError:
                # connection failure
                raise IOError("Could not connect to the source.\n"
                              "Check for a working internet connection?")

            else:

                # load response into dict
                data = response.read()
                response_dict = json.loads(data)

                # check for errors
                if ('status' in response_dict and
                    response_dict['status'] == 'ERROR'):

                    # query field errors
                    for error in response_dict['errors']:
                        log.error(" - field error: {}".format(error))
                    raise IOError(
                        "A configuration error occured, see log for details")

                elif 'message' in response_dict:

                    # message from API came back
                    message = response_dict['message']
                    log.error("An error occured: {}".format(message))
                    raise IOError(message)

                elif ('status' in response_dict and
                      response_dict['status'] == 'OK'):
                    pass  # the okay case is taken care of below

                else:

                    # something unknown happened
                    raise IOError("4 An unknown error occured")

            # when no error occured
            self.hits = response_dict['response']['meta']['hits']
            self.pages = self.hits / 10
            self.offset = response_dict['response']['meta']['offset']
            self.current_page = self.offset / 10
            self.raw_articles = response_dict['response']['docs']
            log.info("Successfully opened resource |"
                     " total number of hits: {} |"
                     " serving [page {}]"
                     .format(self.hits,
                             self.current_page))
            self.storeData()

    def disconnect(self):
        """Disconnect from the source,
        when all hits have been fetched (the current page
        is already the last page) the search on the source
        is finished.

        Otherwise the config parameters are adjusted
        to request the next page
        """
        if not hasattr(self, 'hits'):
            return False
        elif self.current_page >= self.pages:
            return True
        else:
            self.config['page'] = self.current_page + 1
            return False

    def storeData(self):
        """Store the articles in batches
        and write them to a file in the 'json' directory"""
        batch = []
        for article in self.raw_articles:
            # flatten articles and check keys
            flat_article = makeflat.make_flat_structure(article)
            self.checkKeysAgainstSchema(flat_article)
            batch.append(flat_article)

        batchfilename = '.'.join([self.outputfilename,
                                  str(self.current_page), 'json'])
        batchfile = os.path.join(
            JSON_DIR, batchfilename)
        batch_as_json = json.dumps(batch, indent=4)

        with open(batchfile, 'w') as outfile:
            outfile.write(batch_as_json)

        log.debug("write batch as json {}"
                  .format(batch_as_json))
        log.info(u'wrote {1} articles to {0}'.format(
            batchfilename, len(batch)))
        self.batches.append(batch)

    def getDataBatch(self):
        """
        Generator - Get data from source on batches.
        :returns One list for each batch. Each of those is a list of
                 dictionaries with the defined rows.
        holt alle news artikel und schreibt sie in eine Liste
        """
        log.info(u'getBatchData from {} batches'.format(len(self.batches)))

        for batch in self.batches:
            yield batch

    def checkKeysAgainstSchema(self, flat_article):
        """
        The keys are checked against the known data schema
        to spot new fields or values.

        New fields or values are logged as warnings

        The flattend articles attributes names are taken as
        starting point for the check
        """
        for key, value in flat_article.items():

            # mainly the first part of the key should be know as a
            # field in the schema
            keyparts = key.split('.')

            if (key == 'type_of_material' and NYT_REPORT_UNKNOWN_VALUES and
                value not in nyt_constants.TYPE_OF_MATERIAL):
                log.warning(u'Unknown data value "{}" detected for key: "{}"'
                            .format(value, key))

            elif (key == 'new_desk' and NYT_REPORT_UNKNOWN_VALUES and
                  value not in nyt_constants.NEW_DESK):
                log.warning(u'Unknown data value "{}" detected for key: "{}"'
                            .format(value, key))

            elif (key == 'section_name' and NYT_REPORT_UNKNOWN_VALUES and
                  value not in nyt_constants.SECTION_NAME):
                log.warning(u'Unknown data value "{}" detected for key: "{}"'
                            .format(value, key))

            elif (len(keyparts) == 1 and
                  key not in self.getSchema()):
                log.warning(u'Unknown data key detected: {}'.format(key))

            elif (keyparts[0] in ['headline', 'byline'] and
                  key not in self.getSchema()):
                log.warning(u'Unknown data key detected: {}'.format(key))

            elif (keyparts[0] in ['keywords', 'multimedia'] and
                  '.'.join([keyparts[0], '0', keyparts[2]])
                  not in self.getSchema()):
                log.warning(u'Unknown data key detected: {}'.format(key))

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source.

        These are the known first level columns of the source.

        The result is not flat, so 'headline' or 'byline' come with a nested
        structure that is flattened and then written to the json output file
        as 'headline.main', 'headline.print_line', etc.

        Other fields such as 'keywords' and 'multimedia' come as lists.
        They are flattened as 'keywords.0.rank, keywords.1.rank, etc.

        This schema here refers to the original data and is meant to
        check against for new fields in the API.
        """
        schema = [
            'score',
            'print_page',
            'type_of_material',
            '_id',
            'headline.main',
            'headline.print_headline',
            'headline.kicker',
            'byline.original',
            'new_desk',
            'document_type',
            'pub_date',
            'type_of_material',
            'print_page',
            'score',
            'word_count',
            'snippet',
            'source',
            'web_url',
            'keywords.0.rank',
            'keywords.0.is_value',
            'keywords.0.isMajor',
            'keywords.0.name',
            'keywords.0.value',
            'multimedia.0.width',
            'multimedia.0.url',
            'multimedia.0.rank',
            'multimedia.0.height',
            'multimedia.0.subtype',
            'multimedia.0.type',
            'multimedia.0.legacy',
            'abstract',
            'section_name',
            'uri'
        ]

        return schema
