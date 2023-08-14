from utils.webdriver import start_webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


class HTML:
    SEARCH_FIELD = "//input[@name='q']"
    SEARCH_BUTTON = "//button[@type='submit']"
    TWEET_TEXT = ".tweet-content"
    SHOW_MORE_BUTTON = "//div[@class='show-more']"


def search_tweets(query: str, limit: int = 100) -> list:
    
    driver = start_webdriver() # Start webdriver
    driver.get("https://nitter.net/search?") # Get to search page
    
    tweets_corpus = []
    try:
        _search_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, HTML.SEARCH_FIELD))).send_keys(query) # Input user's query to search field
        
        _search_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, HTML.SEARCH_BUTTON))).click() # Find and click search button
        
        while True:
            # Try to find the "show more" button and click it
            load_more_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, HTML.SHOW_MORE_BUTTON))) 
            
            # Parser HTML page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Get all tweet div
            tweets = soup.find_all('div', class_='timeline-item')
            for tweet in tweets:
                try:
                    username = tweet.find('a', class_='username').get_text() # Scrapped username
                    tweet_text = tweet.find('div', class_='tweet-content').get_text() # Scrapped tweet text
                    tweet_time = tweet.find('span', class_='tweet-date').find('a')['title'] # Scrapped time
                    
                    tweets_corpus.append(
                        {'time':tweet_time,
                        'tweet':tweet_text,
                        'username':username}
                    ) # Append data to tweets_corpus: list
                    
                except AttributeError: # Skip first tweet component after n+1 pages, beacuse its not containing scrapped element
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
    