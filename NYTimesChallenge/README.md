# New York Times Article API: Dataloader

## Requirements

- It is assumed you have **Python 2.7** installed on your machine

## Install
- Unzip the directory and then go into the directory

## Get Api Key

- Get yourself an api key from the New York Times API
[link for getting an api key](https://developer.nytimes.com/signup)

## Usage

- Start dataloader with the following command:
```
python2 nytbatches.py 5 <your-api-key> -b 20170414 -e 20170415 -q Facebook
```

### Required arguments:
- the **number of batches**, you request (one batch consists of 10 articles)
- **your api key**

### Optional arguments
- date **b** egin search
- date **e** nd search
- **q** ueryterm

## Result

### Batches
- You will receive the requested number of batches
- Or as many batches as needed to serve
all hits from your query.

### Where are the Articles?

- On screen only headers and ids are displayed.

- You find the complete flattend articles in the batch-files in the `json` directory

- The result of the query above would be stored in files with the following names:
```
q-facebook-begin_date-20170414-end_data-20170415.0.json
q-facebook-begin_date-20170414-end_date-20170415.1.json
...
```
- Each batch contains 10 or less articles

## Flattend Structure of Articles
- The programm `makeflat.py` flattens the articles or any structure
of python dictionaries and lists recursively

- **Nested dictionaries** are turned into a flat dictonary with combined keys:
```
{'headline': {'main': 'some headline', 'kicker': 'some excitement'}}
```
is turned into:
```
{'headline.main': 'some headline',
'headline.kicker': 'some excitement'}
```
- **List items** get keys, that are derived by numbering the items:
```
{'keywords': [{'value': 'US', rank': 1}, {'value': 'Soccer', rank': 2}]}
```
is turned into:
```
{'keywords.0.value': 'US',
 'keywords.0.rank': 1,
 'keywords.1.value': 'Soccer',
 'keywords.1.rank': 2}
```

## Tests
- `makeflat.py` is fully tested:
- Run the tests with `python2 -m unittest discover`

- The dataloader does not have tests yet.

## On the New York Times Article API

### Supported Queries
- the API supports quite sophisticated query logic with Lucene
[see here for details](http://developer.nytimes.com/article_search_v2.json#/README)
- the **fields** are documented
[here](http://developer.nytimes.com/article_search_v2.json#/Documentation)
at this location you can also try queries and watch how the query parameters are set
in different programming languages
- returns always a batch of 10 articles or less
- the total number of **hits** and the **offset** are returned as well
- the **offset** is 0 for the first page
- **subsequent pages** can be requested by including the `page`
query parameter

### Detecting Connection Errors
- the **status** returned by the API will be either 'OK' or 'ERROR'
- in case of 'ERROR' a list of `errors` comes back
- in some cases there will be just a `message` coming back,
for example when the API Rate Limit is reached.
