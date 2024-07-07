# nitter-harvest

A Python library for scraping data from Nitter.net, a Twitter mirror site. Uses Selenium and BeautifulSoup for efficient data extraction.

## Setup

1. Install Firefox and geckodriver. [Tutorial](https://www.youtube.com/watch?v=4NxqmX6F6po)
2. Clone this repository

## Usage

Create a new Python file or Jupyter notebook in the same directory as the `nitter-harvest` folder.

### Profile Scraper

```python
from nitterharvest.profileScrapper import profile_tweets

tweets = profile_tweets(username='jokowi', limit=50)
```

### Topic/Hashtag Scraper

```python
from nitterharvest.searchScrapper import search_tweets

query = "#jokowi lang:id since:2020-10-20"
tweets = search_tweets(query=query, limit=50)
```

Both functions return a list of dictionaries containing tweet data:

```python
[
    {
        'time': 'Aug 12, 2023 · 10:37 AM UTC',
        'tweet': 'Tweet content...',
        'username': '@user'  # Only for search_tweets
    },
    # ...
]
```

## Note

This tool is for educational purposes only. Respect website terms of service and Twitter's policies when using scraped data.
