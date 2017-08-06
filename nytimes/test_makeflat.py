# -*- coding: utf-8 -*-
"""
this file contains the tests for makeflat.py
"""
import unittest

import makeflat

# testdata
empty_dict = {}
transformed_empty_dict = empty_dict
simple_dict = {'a': 1, 'b': 2}
transformed_simple_dict = simple_dict
nested_dict1 = {
    'a': 1,
    'b': {'c': 2}}
transformed_nested_dict1 = {
    'a': 1,
    'b.c': 2}
nested_dict2 = {
    'a': 1,
    'b': {'c': {'d': 2}}}
transformed_nested_dict2 = {
    'a': 1,
    'b.c.d': 2}
nested_dict_with_list = {
    'a': 1,
    'b': [{'c': 2}, {'d': 3}],
    'e': 8}
transformed_nested_dict_with_list = {
    'a': 1,
    'b.0.c': 2, 'b.1.d': 3,
    'e': 8}
nested_dict_with_empty_structures = {
    'a': 1,
    'x': [],
    'y': {},
    'b': [{'c': 2}, {'d': 3}],
    'e': 8}
transformed_nested_dict_with_empty_structures = {
    'a': 1,
    'e': 8,
    'b.0.c': 2, 'b.1.d': 3
}

# testdata from the original source
query_result_simple = {
    "web_url": "https://www.nytimes.com/reuters/2017/08/03/world/africa/03reuters-safrica-politics.html",
    "snippet": "The woman who will decide whether to allow a secret ballot that could oust South African President Jacob Zuma was quoted on Thursday saying she would \"do the right thing\".",
    "blog": {},
    "source": "Reuters",
    "multimedia": [],
    "headline": {
      "main": "Speaker Promises to 'Do the Right Thing' on Move to Oust South Africa's Zuma",
      "print_headline": "Speaker Promises to 'Do the Right Thing' on Move to Oust South Africa's Zuma"
    },
    "keywords": [],
    "pub_date": "2017-08-03T11:42:39+0000",
    "document_type": "article",
    "new_desk": "None",
    "section_name": "Africa",
    "byline": {
      "original": "By REUTERS"
    },
    "type_of_material": "News",
    "_id": "59830c3995d0e0246f1fde44",
    "word_count": 300,
    "score": 1,
    "uri": "nyt://article/ab2b6cc8-4126-58fa-892c-668de489a80c"
}
transformed_query_result_simple = {
 'type_of_material': 'News',
 'document_type': 'article',
 'web_url': 'https://www.nytimes.com/reuters/2017/08/03/world/africa/03reuters-safrica-politics.html',
 'headline.print_headline': "Speaker Promises to 'Do the Right Thing' on Move to Oust South Africa's Zuma",
 'pub_date': '2017-08-03T11:42:39+0000',
 'uri': 'nyt://article/ab2b6cc8-4126-58fa-892c-668de489a80c',
 'word_count': 300,
 'snippet': 'The woman who will decide whether to allow a secret ballot that could oust South African President Jacob Zuma was quoted on Thursday saying she would "do the right thing".',
 'source': 'Reuters',
 'score': 1,
 'section_name': 'Africa',
 'byline.original': 'By REUTERS',
 'new_desk': 'None',
 '_id': '59830c3995d0e0246f1fde44',
 'headline.main': "Speaker Promises to 'Do the Right Thing' on Move to Oust South Africa's Zuma"}
query_result_complex = {
        "web_url": "https://www.nytimes.com/2017/07/11/business/the-deep-industry-ties-of-trumps-deregulation-teams.html",
        "snippet": "A campaign to cut government rules is being conducted largely out of public view, often by hires with potential conflicts, an investigation has found.",
        "print_page": "1",
        "blog": {},
        "source": "The New York Times",
        "multimedia": [
          {
            "type": "image",
            "subtype": "xlarge",
            "url": "images/2017/07/11/us/11trumpethics/11trumpethics-articleLarge.jpg",
            "height": 399,
            "width": 600,
            "rank": 0,
            "legacy": {
              "xlargewidth": 600,
              "xlarge": "images/2017/07/11/us/11trumpethics/11trumpethics-articleLarge.jpg",
              "xlargeheight": 399
            }
          },
          {
            "type": "image",
            "subtype": "wide",
            "url": "images/2017/07/11/us/11trumpethics/11trumpethics-thumbWide.jpg",
            "height": 126,
            "width": 190,
            "rank": 0,
            "legacy": {
              "wide": "images/2017/07/11/us/11trumpethics/11trumpethics-thumbWide.jpg",
              "widewidth": 190,
              "wideheight": 126
            }
          },
          {
            "type": "image",
            "subtype": "thumbnail",
            "url": "images/2017/07/11/us/11trumpethics/11trumpethics-thumbStandard.jpg",
            "height": 75,
            "width": 75,
            "rank": 0,
            "legacy": {
              "thumbnailheight": 75,
              "thumbnail": "images/2017/07/11/us/11trumpethics/11trumpethics-thumbStandard.jpg",
              "thumbnailwidth": 75
            }
          }
        ],
        "headline": {
          "main": "The Deep Industry Ties of Trump’s Deregulation Teams",
          "kicker": "Trump Rules",
          "print_headline": "The Deep Industry Connections Of Trump’s Deregulation Teams"
        },
        "keywords": [
          {
            "isMajor": "N",
            "rank": 1,
            "name": "persons",
            "value": "Trump, Donald J"
          },
          {
            "isMajor": "N",
            "rank": 2,
            "name": "subject",
            "value": "United States Politics and Government"
          },
          {
            "isMajor": "N",
            "rank": 3,
            "name": "subject",
            "value": "Regulation and Deregulation of Industry"
          },
          {
            "isMajor": "N",
            "rank": 4,
            "name": "subject",
            "value": "Appointments and Executive Changes"
          },
          {
            "isMajor": "N",
            "rank": 5,
            "name": "subject",
            "value": "Conflicts of Interest"
          },
          {
            "isMajor": "N",
            "rank": 6,
            "name": "organizations",
            "value": "Agriculture Department"
          },
          {
            "isMajor": "N",
            "rank": 7,
            "name": "organizations",
            "value": "Education Department (US)"
          },
          {
            "isMajor": "N",
            "rank": 8,
            "name": "organizations",
            "value": "Energy Department"
          },
          {
            "isMajor": "N",
            "rank": 9,
            "name": "organizations",
            "value": "Environmental Protection Agency"
          },
          {
            "isMajor": "N",
            "rank": 10,
            "name": "organizations",
            "value": "Government Accountability Office"
          },
          {
            "isMajor": "N",
            "rank": 11,
            "name": "organizations",
            "value": "Interior Department"
          },
          {
            "isMajor": "N",
            "rank": 12,
            "name": "organizations",
            "value": "Housing and Urban Development Department"
          },
          {
            "isMajor": "N",
            "rank": 13,
            "name": "subject",
            "value": "Endangered and Extinct Species"
          },
          {
            "isMajor": "N",
            "rank": 14,
            "name": "subject",
            "value": "Lobbying and Lobbyists"
          },
          {
            "isMajor": "N",
            "rank": 15,
            "name": "organizations",
            "value": "Syngenta AG"
          },
          {
            "isMajor": "N",
            "rank": 16,
            "name": "subject",
            "value": "Pesticides"
          },
          {
            "isMajor": "N",
            "rank": 17,
            "name": "persons",
            "value": "Cameron, Scott J"
          },
          {
            "isMajor": "N",
            "rank": 18,
            "name": "persons",
            "value": "Dravis, Samantha"
          },
          {
            "isMajor": "N",
            "rank": 19,
            "name": "persons",
            "value": "Kasper, Maren"
          },
          {
            "isMajor": "N",
            "rank": 20,
            "name": "persons",
            "value": "McCormack, Brian"
          }
        ],
        "pub_date": "2017-07-11T09:00:38+0000",
        "document_type": "article",
        "new_desk": "Business",
        "byline": {
          "original": "By DANIELLE IVORY and ROBERT FATURECHI"
        },
        "type_of_material": "News",
        "_id": "596493bd95d0e0246f1f9c12",
        "word_count": 2823,
        "score": 7.9840384,
        "uri": "nyt://article/b5a61602-73bd-59de-86ba-9430e14a81a4"
      }
transformed_query_result_complex = {
     'keywords.0.value': 'Trump, Donald J', 'word_count': 2823, 'keywords.7.value': 'Energy Department',
     'keywords.13.rank': 14, 'keywords.10.rank': 11, 'keywords.15.value': 'Pesticides',
     'keywords.18.value': 'Kasper, Maren', 'keywords.5.rank': 6, 'multimedia.2.legacy.thumbnailwidth': 75,
     'keywords.14.isMajor': 'N', 'source': 'The New York Times', 'keywords.12.name': 'subject',
     'keywords.4.isMajor': 'N', 'keywords.8.rank': 9, 'keywords.18.rank': 19,
     'keywords.14.value': 'Syngenta AG', 'keywords.5.value': 'Agriculture Department',
     'keywords.19.name': 'persons', 'keywords.13.isMajor': 'N', 'keywords.6.rank': 7,
     'keywords.18.isMajor': 'N', 'multimedia.1.rank': 0, 'multimedia.1.type': 'image',
     'multimedia.1.legacy.wideheight': 126,
     'multimedia.1.legacy.wide': 'images/2017/07/11/us/11trumpethics/11trumpethics-thumbWide.jpg',
     'document_type': 'article', 'new_desk': 'Business', 'keywords.8.value': 'Environmental Protection Agency',
     'keywords.7.rank': 8, 'multimedia.0.rank': 0, 'keywords.2.name': 'subject',
     'keywords.13.value': 'Lobbying and Lobbyists', 'multimedia.0.legacy.xlargeheight': 399,
     'headline.print_headline': 'The Deep Industry Connections Of Trump\xe2\x80\x99s Deregulation Teams',
     'multimedia.2.legacy.thumbnailheight': 75, 'multimedia.2.width': 75, 'multimedia.0.width': 600,
     'keywords.10.name': 'organizations',
     'web_url': 'https://www.nytimes.com/2017/07/11/business/the-deep-industry-ties-of-trumps-deregulation-teams.html',
     'keywords.2.value': 'Regulation and Deregulation of Industry', 'keywords.15.isMajor': 'N',
     'multimedia.0.legacy.xlargewidth': 600,
     'multimedia.0.legacy.xlarge': 'images/2017/07/11/us/11trumpethics/11trumpethics-articleLarge.jpg',
     'keywords.0.isMajor': 'N', 'multimedia.1.height': 126, 'multimedia.0.type': 'image', 'score': 7.9840384,
     'keywords.0.rank': 1, 'keywords.11.isMajor': 'N', 'multimedia.1.width': 190, 'keywords.1.rank': 2,
     'byline.original': 'By DANIELLE IVORY and ROBERT FATURECHI',
     'multimedia.2.url': 'images/2017/07/11/us/11trumpethics/11trumpethics-thumbStandard.jpg',
     'keywords.11.value': 'Housing and Urban Development Department', 'multimedia.2.rank': 0,
     'keywords.12.isMajor': 'N', 'keywords.13.name': 'subject',
     'keywords.3.value': 'Appointments and Executive Changes', 'keywords.17.isMajor': 'N',
     'keywords.10.isMajor': 'N', 'keywords.18.name': 'persons',
     'multimedia.0.url': 'images/2017/07/11/us/11trumpethics/11trumpethics-articleLarge.jpg',
     'keywords.14.name': 'organizations', 'keywords.3.name': 'subject',
     'headline.main': 'The Deep Industry Ties of Trump\xe2\x80\x99s Deregulation Teams',
     'keywords.9.name': 'organizations', 'keywords.0.name': 'persons', 'type_of_material': 'News',
     'keywords.4.rank': 5, 'keywords.8.name': 'organizations', 'print_page': '1',
     'headline.kicker': 'Trump Rules',
     'multimedia.2.legacy.thumbnail': 'images/2017/07/11/us/11trumpethics/11trumpethics-thumbStandard.jpg',
     'multimedia.0.height': 399, 'keywords.17.rank': 18, 'keywords.8.isMajor': 'N',
     'multimedia.1.subtype': 'wide', 'multimedia.0.subtype': 'xlarge', 'multimedia.2.type': 'image',
     'keywords.16.name': 'persons', 'keywords.6.name': 'organizations', 'keywords.11.rank': 12,
     'keywords.10.value': 'Interior Department', 'keywords.7.isMajor': 'N',
     'keywords.4.value': 'Conflicts of Interest', 'keywords.12.value': 'Endangered and Extinct Species',
     'keywords.14.rank': 15, 'keywords.16.rank': 17, 'keywords.7.name': 'organizations', 'keywords.3.rank': 4,
     'keywords.15.name': 'subject', 'keywords.17.value': 'Dravis, Samantha', 'keywords.15.rank': 16,
     'keywords.4.name': 'subject', 'keywords.16.value': 'Cameron, Scott J',
     'multimedia.1.legacy.widewidth': 190, 'keywords.19.rank': 20, 'keywords.1.name': 'subject',
     'keywords.19.value': 'McCormack, Brian', 'keywords.6.isMajor': 'N', 'multimedia.2.subtype': 'thumbnail',
     'keywords.6.value': 'Education Department (US)',
     'keywords.1.value': 'United States Politics and Government', 'keywords.11.name': 'organizations',
     'multimedia.1.url': 'images/2017/07/11/us/11trumpethics/11trumpethics-thumbWide.jpg',
     'keywords.2.isMajor': 'N', 'multimedia.2.height': 75, 'keywords.5.isMajor': 'N',
     'snippet': 'A campaign to cut government rules is being conducted largely out of public view, often by hires with potential conflicts, an investigation has found.',
     'keywords.5.name': 'organizations', 'keywords.9.rank': 10, 'keywords.17.name': 'persons',
     'keywords.1.isMajor': 'N', 'keywords.9.value': 'Government Accountability Office',
     'keywords.19.isMajor': 'N', 'keywords.2.rank': 3, 'keywords.3.isMajor': 'N',
     'pub_date': '2017-07-11T09:00:38+0000', 'keywords.16.isMajor': 'N',
     'uri': 'nyt://article/b5a61602-73bd-59de-86ba-9430e14a81a4', 'keywords.9.isMajor': 'N',
     '_id': '596493bd95d0e0246f1f9c12', 'keywords.12.rank': 13}


class TestMakeFlat(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_structure_depth_empty_dictionary(self):
        """empty dictionary above has depth 0"""
        self.assertEquals(makeflat.get_structure_depth(empty_dict), 0)

    def test_get_structure_depth_simple_dictionary(self):
        """simple dictionary above has depth 1"""
        self.assertEquals(makeflat.get_structure_depth(simple_dict), 1)

    def test_get_structure_depth_nested_dict1(self):
        """nested dictionary 1 above has depth 2"""
        self.assertEquals(makeflat.get_structure_depth(nested_dict1), 2)

    def test_get_structure_depth_nested_dict2(self):
        """nested dictionary 2 above has depth 3"""
        self.assertEquals(makeflat.get_structure_depth(nested_dict2), 3)

    def test_get_structure_depth_nested_dict_with_list(self):
        """nested dictionary with list above has depth 3"""
        self.assertEquals(makeflat.get_structure_depth(
            nested_dict_with_list), 3)

    def test_get_structure_depth_query_result_simple(self):
        """simple query result above has depth 2"""
        self.assertEquals(makeflat.get_structure_depth(query_result_simple), 2)

    def test_get_structure_depth_query_result_complex(self):
        """complex query result above has depth 4"""
        self.assertEquals(makeflat.get_structure_depth(
            query_result_complex), 4)

    def test_makeflat_structure_empty_dict(self):
        """empty dictionary is already flat: remains the same"""
        self.assertDictEqual(
            makeflat.make_flat_structure(empty_dict),
            empty_dict
        )

    def test_makeflat_structure_simple_dictionary(self):
        """simple dictionary above is already flat: remains the same"""
        self.assertDictEqual(
            makeflat.make_flat_structure(simple_dict),
            simple_dict
        )

    def test_makeflat_structure_nested_dict1(self):
        """nested dictionary 1 above will be transformed into a flat dict"""
        self.assertDictEqual(
            makeflat.make_flat_structure(nested_dict1),
            transformed_nested_dict1
        )

    def test_makeflat_structure_nested_dict2(self):
        """nested dictionary 2 above will be transformed into a flat dict"""
        self.assertDictEqual(
            makeflat.make_flat_structure(nested_dict2),
            transformed_nested_dict2
        )

    def test_makeflat_structure_nested_dict_with_list(self):
        """nested dictionary with list above
        will be transformed into a flat dict"""
        self.assertDictEqual(
            makeflat.make_flat_structure(nested_dict_with_list),
            transformed_nested_dict_with_list
        )

    def test_makeflat_nested_dict_with_empty_structures(self):
        """nested dictionary with list above will be
        transformed into a flat dict"""
        self.assertDictEqual(
            makeflat.make_flat_structure(nested_dict_with_empty_structures),
            transformed_nested_dict_with_empty_structures
        )

    def test_makeflat_structure_query_result_simple(self):
        """simple query result above will be transformed into a flat dict"""
        self.assertDictEqual(
            makeflat.make_flat_structure(query_result_simple),
            transformed_query_result_simple
        )

    def test_makeflat_structure_query_result_complex(self):
        """complex query result above will be transformed into a flat dict"""
        self.assertDictEqual(
            makeflat.make_flat_structure(query_result_complex),
            transformed_query_result_complex
        )
