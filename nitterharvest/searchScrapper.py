# utils
from .utils.webdriver import start_webdriver
from .utils.html_element import LOAD_MORE, SEARCH, TWEET

# webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# scrapper
from bs4 import BeautifulSoup


def search_tweets(query: str, limit: int = 100) -> list:
    """scrapper for hashtag, topic, search query tweets

    Args:
        query (str): user's search query
        limit (int, optional): max tweets to scrape. Defaults to 100.

    Returns:
        list[dict]: scrapped tweet's => [
            "time",
            "tweet",
            "username"
        ]
    """
    
    driver = start_webdriver() # Start webdriver
    driver.get("https://nitter.net/search?") # Get to search page
    print("=== searching... ===")
    
    tweets_corpus = []
    try:
        _search_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, SEARCH.FIELD))).send_keys(query) # Input user's query to search field
        
        _search_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, SEARCH.BUTTON))).click() # Find and click search button
        
        while True:
            # Try to find the "show more" button and click it
            load_more_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, LOAD_MORE.BUTTON))) 
            
            # Parser HTML page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Get all tweet div
            tweets = soup.find_all('div', class_=TWEET.CONTAINER)
            for tweet in tweets:
                try:
                    username = tweet.find('a', class_=TWEET.USERNAME).get_text() # Scrapped username
                    tweet_text = tweet.find('div', class_=TWEET.TEXT).get_text() # Scrapped tweet text
                    tweet_time = tweet.find('span', class_=TWEET.TIME).find('a')['title'] # Scrapped time
                    
                    tweets_corpus.append(
                        {
                            'time':tweet_time,
                            'tweet':tweet_text,
                            'username':username
                        }
                    ) # Append data to tweets_corpus: list
                
                # Skip first tweet component after n+1 pages, beacuse its not containing scrapped element    
                except AttributeError: 
                    continue
                
            # click show more / next page
            load_more_button.click()
            print(f"Tweets scraped: {len(tweets_corpus)}")
            
            # Limit n scrapped tweets
            if len(tweets_corpus) >= limit:
                print("=== done! ===")
                
                print(f"success scrapping {len(tweets_corpus)} tweets")
                break
    
    # If there's no element left to scrape then error -> scrapped finish
    except Exception as _:
        print("Finished loading all content or an error occurred:", str(_))
        
    
    # scraped tweets
    return tweets_corpus
