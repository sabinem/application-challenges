"""
Constants for the NY Times API

- the url for the API access

- some fields with discrete values,
that have been published in the API's documentation:
at http://developer.nytimes.com/article_search_v2.json#/README
"""

# the Url for the Article API
NYTIMES_ARTICLES_URL = \
    'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# 'type_of_material' is an article field with discrete values
TYPE_OF_MATERIAL = [
    "Addendum", "An Analysis", "An Appraisal", "Article",
    "Banner", "Biography", "Birth Notice",
    "Blog", "Brief", "briefing",
    "Caption", "Chronology", "Column",
    "Correction", "Economic Analysis",
    "Editorial", "Editorial Cartoon",
    "Editors' Note", "First Chapter",
    "Front Page", "Glossary",
    "Interactive Feature",
    "Interactive Graphic",
    "Interview",
    "Letter", "List",
    "Marriage Announcement",
    "Military Analysis",
    "News", "News Analysis",
    "Newsletter", "Obituary",
    "Obituary (Obit)", "Op-Ed",
    "Paid Death Notice", "Postscript", "Premium",
    "Question", "Quote", "Recipe", "Review", "Schedule",
    "SectionFront", "Series",
    "Slideshow", "Special Report",
    "Statistics", "Summary",
    "Text", "Video", "Web Log"
]

# 'section_name' is an article field with discrete values
SECTION_NAME = [
    "Arts", "Automobiles", "Autos",
    "Blogs", "Books", "Book Review", "Booming",
    "Business", "Business Day",
    "Corrections", "Crosswords & Games",
    "Crosswords/Games", "Dining & Wine",
    "Dining and Wine", "Editors' Notes",
    "Education", "Europe", "Fashion & Style",
    "Food", "Front Page",
    "Giving", "Global Home",
    "Great Homes & Destinations",
    "Great Homes and Destinations",
    "Health", "Home & Garden",
    "Home and Garden", "International Home",
    "Job Market", "Learning",
    "Magazine",  "Media", "Middle East", "Movies",
    "Multimedia", "Multimedia/Photos",
    "N.Y. / Region", "N.Y./Region", "NYRegion",
    "NYT Now", "National", "New York",
    "New York and Region", "Obituaries",
    "Olympics", "Open", "Opinion",
    "Paid Death Notices", "Public Editor",
    "Real Estate", "Science", "Sports",
    "Style", "Sunday Magazine", "Sunday Review",
    "T Magazine", "T:Style", "Technology",
    "The Public Editor", "The Upshot",
    "Theater", "Times Topics",
    "TimesMachine", "Today's Headlines",
    "Topics", "Travel", "U.S.",
    "Universal", "UrbanEye", "Washington", "Weddings",
    "Week in Review", "World", "Your Money"
]

# 'new_desk' is an article field with discrete values
NEW_DESK = [
    "Adventure Sports", "Arts & Leisure",
    "Arts", "Automobiles",
    "Blogs", "Books", "Booming",
    "Business Day", "Business", "Cars",
    "Circuits", "Classifieds",
    "Connecticut", "Crosswords & Games",
    "Culture", "DealBook", "Dining",
    "Editorial", "Education", "Energy",
    "Entrepreneurs", "Environment", "Escapes",
    "Fashion & Style", "Fashion", "Favorites",
    "Financial", "Flight", "Food",
    "Foreign", "Generations",
    "Giving", "Global Home",
    "Health & Fitness", "Health",
    "Home & Garden", "Home",
    "Jobs", "Key",
    "Letters", "Long Island",
    "Magazine", "Market Place",
    "Men's Health",
    "Metro", "Metropolitan",
    "Movies", "Museums",
    "National", "Nesting", "None",
    "Obits", "Obituaries", "Obituary",
    "OpEd", "Opinion",
    "Outlook", "Personal Investing",
    "Personal Tech", "Play",
    "Politics", "Regionals",
    "Retail", "Retirement",
    "Science", "Small Business", "Soccer",
    "Society", "Sports",
    "Style", "Sunday Business",
    "Sunday Review", "Sunday Styles",
    "T Magazine", "T Style",
    "Technology", "Teens",
    "Television", "The Arts",
    "The Business of Green",
    "The City Desk", "The City",
    "The Marathon", "The Millennium",
    "The Natural World", "The Upshot",
    "The Weekend", "The Year in Pictures",
    "Theater", "Then & Now", "Thursday Styles",
    "Times Topics", "Travel", "U.S.",
    "Universal", "Upshot",
    "UrbanEye", "Vacation",
    "Washington", "Wealth", "Weather",
    "Week in Review", "Week", "Weekend",
    "Westchester", "Wireless Living",
    "Women's Health", "Working",
    "Workplace", "World", "Your Money"
]
