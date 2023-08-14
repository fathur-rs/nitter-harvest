# utils
from .utils.webdriver import start_webdriver
from .utils.html_element import LOAD_MORE, TWEET

# webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# scrapper
from bs4 import BeautifulSoup


def profile_tweets(username: str, limit: int = 100) -> list:
    """scrapper for profile's tweets

    Args:
        username (str): twitter username
        limit (int, optional): max tweets to scrape. Defaults to 100.

    Returns:
        list[str]: scrapped tweet's => [
            "time",
            "tweets"
        ]
    """
    
    driver = start_webdriver() # Webdriver
    driver.get('https://nitter.net/' + username) # Redirect to user's profile page
    print("=== redirect to tweets profile ===")
    
    tweets_corpus = [] # Containing scrapped tweets
    try:
        while True:
            # Try to find the "show more" button and click it
            load_more_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, LOAD_MORE.BUTTON)))
            
            # Parser HTML page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            tweets = soup.find_all('div', class_=TWEET.CONTAINER)
            for tweet in tweets:
                try:
                    tweet_text = tweet.find('div', class_=TWEET.TEXT).get_text() # Scrapped tweet text
                    
                    tweet_time = tweet.find('span', class_=TWEET.TIME).find('a')['title'] # Scrapped time
                    
                    tweets_corpus.append(
                        {
                            'time':tweet_time,
                            'tweet':tweet_text
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
        
    return tweets_corpus
