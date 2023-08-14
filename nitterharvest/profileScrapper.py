from utils.webdriver import start_webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class HTML:
    SHOW_MORE_BUTTON = "//div[@class='show-more']"
    TWEET_TEXT = ".tweet-content"


def profile_tweets(username: str, limit: int = 100) -> list:
    """scrapper for profile's tweets

    Args:
        username (str): twitter username
        limit (int, optional): max tweets to scrape. Defaults to 100.

    Returns:
        list: tweets
    """
    
    driver = start_webdriver() # Webdriver
    driver.get('https://nitter.net/' + username) # Redirect to user's profile page
    print("=== redirect to tweets profile ===")
    
    tweets_corpus = [] # Containing scrapped tweets
    try:
        while True:
            # Try to find the "show more" button and click it
            load_more_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, HTML.SHOW_MORE_BUTTON)))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tweets = soup.select(HTML.TWEET_TEXT)
            for tweet in tweets:
                tweets_corpus.append(tweet.get_text())
                
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

