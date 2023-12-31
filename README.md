# nitter-harvest
**nitter-harvest** is a library designed to scrape data from Nitter.net, which serves as a mirror for Twitter. The library leverages the power of both Selenium and BeautifulSoup to efficiently extract the desired data.

# how to use?
1. Download Firefox browser and geckodriver then, installed it. You can find the tutorial right here: [Tutorial](https://www.youtube.com/watch?v=4NxqmX6F6po).
2. Clone the repository.
3. cd to nitter-harvest
4. Create new .py or .ipynb. Like below.
#####
    Directory
    nitter-harvest # Cloned Repo, cd to nitter-harvest
    │
    ├── nitterharvest # scrapping module
    │
    └── <your-code>.py/ipynb # your code

# use case
### 1. Profile Scrapper
```python
from nitterharvest.profileScrapper import profile_tweets

tweets = profile_tweets(username='jokowi', limit=50)

# output 

#[{'time': 'Aug 12, 2023 · 10:37 AM UTC',
#  'tweet': 'Kebijakan hilirisasi mendapat tantangan...'},
# {'time': 'Aug 10, 2023 · 12:25 PM UTC',
#  'tweet': 'Indonesia membutuhkan pemimpin..},
#  ...]
```
### 2. Topic, Hashtag Scrapper
```python
from nitterharvest.searchScrapper import search_tweets

query = "#jokowi lang:id since:2020-10-20"
tweets = search_tweets(query=query, limit=50)

# output 

#[{'time': 'Oct 19, 2020 · 8:23 PM UTC',
#  'tweet': 'Gua jadi bertanya dlm hati\nKok demo..,
#  'username': '@Fajar_Bumaye'},
#  {'time': 'Oct 19, 2020 · 6:42 PM UTC',
#  'tweet': 'terimakasih pak jokowi at..,
#  'username': '@Ajacan1'},
#  ...]
```
