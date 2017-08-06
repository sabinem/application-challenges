# -*- coding: utf-8 -*-
"""
Dataloader for NYTimes Article API

- Articles can only be fetched in batches of 10 items

- the Articles are served in these batches of 10

The dataloader is initiated  with a query as
NYTimesSource(**config)

The configuration is supposed to contain the api-key

After initiating the class, the getDataBatch method
can be called with a batch_size. This methods yields
the requested number of batches in articles.

Example:
If NYTimesSource(**config) is configured with a query
that has 235 article hits, 24 batches of 10 articles would be
needed to fetch all the data.

It is possible to request only 10 batches, then only
the first 100 articles will be loaded.

The articles are yielded on screen with their headlines
and ids. They are also written to a file-batches, with
names, that are derived from the query parameters. You find
these batchfiles in the 'json' directory.
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
    makes a recognizable filename from the query dict
    """
    query_parms = [v.lower().replace(" ", "-") for k, v in query.items()]
    return '_'.join(query_parms)


class NYTimesSource(object):
    """
    A data loader plugin for the NY Times API

    Each instance serves one query

    The API brings back only 10 records at a time, but reports the
    total number of hits for the query.

    The records are then fetched in batches of 10 or less record and
    the program goes to sleep for 5 seconds between requests,
    to avoid the rate limit of the API
    """
    def __init__(self, **config):
        """
        The class is initiated by the query it serves

        The queryconfig is the confiq minus the api-key,
        which is supposed to be secret

        The outputfilename for the batchfiles is derived
        from the queryconfig

        The data is fetched in batches of 10 records each
        """
        # The configuration is set
        self.config = config

        # The config is copied to a new config,
        # that does not contain the api-key, since
        # the api-key should not get logged
        self.queryconfig = config.copy()
        self.queryconfig.pop('api-key')

        # The source config is logged
        log.info("configuration with api-key removed: {}"
                 .format(json.dumps(self.queryconfig,
                                    sort_keys=True,
                                    indent=4)))

        # An outputfile name for the batches is preconfigured
        self.outputfilename = make_outputfile_name(self.queryconfig)

    def _connect(self):
        """connects to the API's url
        - get meta data (total hits)
        - get a batch of 10 articles
        - the program goes to sleep between API requests
        in order to avoid the API's rate limit
        """

        # sleep between request to avoid API Rate limit
        time.sleep(5)

        if hasattr(self, 'next_page'):
            self.config['page'] = self.next_page

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
                # the okay case is taken care of below
                pass

            else:

                # something unknown happened
                raise IOError("4 An unknown error occured")

        # When the API call was okay:

        # The hits are only recorded at the first request
        if not hasattr(self, 'hits'):
            self.hits = response_dict['response']['meta']['hits']
            self.pages = self.hits / 10
            if self.hits:
                self.total_nr_batches = self.pages + 1
            else:
                self.total_nr_batches = 0

        # The page and content is updated on every request
        self.offset = response_dict['response']['meta']['offset']
        self.current_page = self.offset / 10
        self.next_page = self.current_page + 1
        self.raw_articles = response_dict['response']['docs']

        # The request is logged
        log.info("Successfully opened resource |"
                 " total number of hits: {} |"
                 " serving [page {}]"
                 .format(self.hits,
                         self.current_page))

        # In debug modus all found article ids are logged
        for article in self.raw_articles:
            log.debug("Article: {}"
                      .format(article['_id']))

    def getDataBatch(self, batch_size):
        """
        Generator
        - Get articles from source in batches of 10
        - check the articles for unknown field or values
        - transform the articles into flat dictionaries,
        (see description in README)
        - write the flat articles as json to a file
        with a recognizable name (see README)
        - yield the articles as batch, before the next
        batch is requested from the source
        """
        log.info("requested: {} batches"
                 .format(batch_size))

        for j in range(batch_size):

            # connect to source
            self._connect()

            # now self.raw_articles is set as a list
            # of the articles, that have just been
            # fetched form the API

            # Next the articles are flattened,
            # the attributes are checked and
            # they are written to a batch
            batch = []
            for article in self.raw_articles:

                # Flatten articles
                flat_article = makeflat.make_flat_structure(article)

                # Check for unknown keys and values
                self._checkKeysAgainstSchema(flat_article)

                # Append flattened article to the batch that
                # will be served
                batch.append(flat_article)

            # The batch is written to a recognizable file
            # that is named with the query parameters

            # Derive the filename
            batchfilename = '.'.join([self.outputfilename,
                                      str(j), 'json'])
            batch_as_json = json.dumps(batch, indent=4)
            batchfile = os.path.join(
                JSON_DIR, batchfilename)

            # Then write the batch to the file
            with open(batchfile, 'w') as outfile:
                outfile.write(batch_as_json)

            # Log that the file has been writen
            log.info(u'wrote {1} articles to {0}'.format(
                batchfilename, len(batch)))

            # Log serving the batch
            log.info("Serving batch of {} articles".format(len(batch)))

            # Serve the batch
            yield batch

            # Break if all batches have been served
            if j > batch_size:
                log.info("Finished after requested batched have been served")
                break

            # Break if all query hits have been served
            if j >= self.pages:
                log.info("Finished after all hits have been served")
                break

    def _checkKeysAgainstSchema(self, flat_article):
        """
        The keys of the flattend articles
        are checked against the known data schema
        of the API:

        The intention is to spot unknown fields or values
        and recognize changes in the API.
        """
        for key, value in flat_article.items():

            # the derived keys are split into parts
            keyparts = key.split('.')

            # it can be set in the settings whether values
            # of discrete fields are compared to the known
            # values in nyt_constants
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

            # firstlevel keys should be known
            elif (len(keyparts) == 1 and
                  key not in self._getSchema()):
                log.warning(u'Unknown data key detected: {}'.format(key))

            # second level keys of nested structure should be known
            elif (keyparts[0] in ['headline', 'byline'] and
                  key not in self._getSchema()):
                log.warning(u'Unknown data key detected: {}'.format(key))

            # second level keys of the list items keywords and
            # multimedia should be known
            elif (keyparts[0] in ['keywords', 'multimedia'] and
                  '.'.join([keyparts[0], '0', keyparts[2]])
                  not in self._getSchema()):
                log.warning(u'Unknown data key detected: {}'.format(key))

    def _getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source.

        This is the schema of the flattend derived article field structure
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
