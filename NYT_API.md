# New York Times Article API: Dataloader

## Analyzing the Source

### General Information:

- the source allows for very differentiated queries with facets and
Lucene syntax

- it will only return 10 articles at a time

- with the articles meta data is returned about the total number of **hits**
for the search. Also the **offset** is returned, being 0 initially.
That means you received page 0 with articles 0-9
- You can then request subsequent pages with the page parameter `page=2`,
which means you are served the hits 20-29.
- to get all hits you need `hit - 1/10` pages:
30 hits means you need 29 / 10 = 2 pages
- size: 16.198.914 hits (accessing the api without query parameters)

### Setting Query parameters
- Setting of the query parameters can be quite advanced due to the Lucene Syntax
and facets that can be used
- in our case I load the data per day, which means `begin_date` and `end_date`
have to differ, otherwise there will be 0 hits. The articles delivered are that
of the begin_date and the end_date is the cut off.


### JSON returned
The response is JSON

#### status
- "OK" for a successful request
#### copyright
- example: "Copyright (c) 2017 The New York Times Company. All Rights Reserved."

#### response:
- the response contains a list of the 10 articles

#### meta
- contains hits, offset and time the request took.
I have already explained hits and offsets above

#### article fields
on the upper level are the following fields: some of these fields
are structured further

##### interesting fields
- _id: internal id identifying the item
- web_url: (str) the excact url for the article
- snippet: (str) text snippet from the article
- source (str) for example "AP"
- pub_date: (YYYY-MM-DD ...) date of publication "2017-05-14T23:57:46+0000" this is actually a timestamp
- byline: original (str) "By Reuters" from what source came the news originally
- headline:
    - main": "Politics, It Seems, Has Jolted Even the Idiot Box Awake",
    - kicker": "Mediator",
    - print_headline": "The Idiot Box, Jolted Awake By Politics"
- document-type: mostly "article", what type of document type is it
   15.614.152 are articles from total of 16.198.914 items
   it makes sense to report other document types encountered
- word_count: count of words
- newsdesk: "None" (495.065 items) or "Foreign" (298.100 items) makes sense to report other cases
- type_of_material: "News" (3.035.438 items)
- abstract: (str): Summary of the article
- print_page: (int) 11
- score: (int) 1
- section_name: "Sunday Review" section in which the artcile occured

##### multimedia
the multimedia come as list with the following fields:
Here is an example:
- type: "image"
- subtype": "thumbnail",
- url": "images/2017/05/15/business/media/15rutenberg1/15rutenberg1-thumbStandard.jpg",
- height": 75,
- width": 75,
- rank": 0,
- legacy:
    - thumbnailheight: 75
    - thumbnail: "images/2017/05/15/business/media/15rutenberg1/15rutenberg1-thumbStandard.jpg"
    - thumbnailwidth: 75

 The legacy field is probably an internal legacy for some api users. They differ depending to the media item
 at hand.


##### keywords
the keywords also come as a list:
- isMajor: "N",
- rank: 1,
- name: "subject" or "persons" or "organizations"
- value: "Television"


##### less interesting fields
- print_page: seems to be 0, cannot be chosen as field
- blog: seems to be {}


##### questionable fields
- lead_paragraph: ?  mentioned in the api description, but not included in the result
- abstract: ? mentioned in the api description, but not included in the result


## Concipating the Dataloader

### Consideration:
- the data can be fetched only 10 articles at a time.
- there are fields, that my serve as faucets, it would be interesting to get a list
of their values
- some fields need to be reformatted

### My dataloader:
- allows the day and a search term as search parameter and fetches the results per day
- logs the ids on a file
- logs the fetched data on a file per day

### flat datastructure:

- _id: internal id identifying the item
- web_url: (str)
- snippet: (str)
- source (str) "AP" -> make list of occurences
- pub_date: (str) "2017-05-14T23:57:46+0000" transform to date
- byline: original (str) "By Reuters" from what source came the news originally
- headline.main (str)
- headline.kicker (str)
- headline.printheadline (str)
- document-type: (str) "article" -> make list of occurences
- word_count: count of words
- newsdesk: "Foreign" -> make list of occurences
- type_of_material: "News" -> make list of occurences
- keyword-0-name, keyword-0-value, keyword-0-is-major, keyword-0-rank;
  the rank could also serve as a key, since the keywords are ranked;
  watch keyword-1-major whether it is always 'N',
- multimedia: I leave the legacy fields aside, they will be numbered, since the rank is mostly 0 in this case
  multimedia-0-type, multimedia-0-subtype, multimedia-0-url, multimedia-0-height, multimedia-0-width,
  multimedia-0-rank
  multimedia-1-type, ...;
  watch the rank: it might be always 0
- blog: {}, only take field if blog is not {}
- print_page: watch if it is always 0


### the algorithmus to flatten the datastructure comes with a test
I build a general algorithmus to flatten data structures