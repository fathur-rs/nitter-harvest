from .utils.webdriver import start_webdriver
from .utils.html_element import HTML
html = HTML()

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


def search_tweets(query: str, limit: int = 100) -> list:
    """
    Scrape tweets based on a search query from nitter.poast.org.

    This function uses Selenium WebDriver to navigate to nitter.poast.org's search page,
    enter a search query, and scrape the resulting tweets. It continuously loads more tweets
    until it reaches the specified limit or there are no more tweets to load.

    Args:
        query (str): The search query (hashtag, topic, or general search term).
        limit (int, optional): The maximum number of tweets to scrape. Defaults to 100.

    Returns:
        list[dict]: A list of dictionaries, each containing information about a single tweet.
                    Each dictionary has the following keys:
                    - 'time': The timestamp of the tweet (str)
                    - 'tweet': The text content of the tweet (str)
                    - 'username': The username of the tweet author (str)

    Raises:
        Exception: If an error occurs during the scraping process. The error message is printed.

    Note:
        - This function requires a working internet connection.
        - The scraping process may take some time depending on the number of tweets requested.
        - The function uses Selenium WebDriver, which must be properly set up in the environment.
        - The HTML class from .utils.html_element is used for locating elements on the page.
    """
    
    driver = start_webdriver() 
    driver.get("https://nitter.poast.org/search?") 
    print(f"=== searching... {query} ===")
    
    tweets_corpus = []
    try:
        _search_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, html.search_field))).send_keys(query) # Input user's query to search field
        
        _search_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, html.search_button))).click() # Find and click search button
        
        while True:
            load_more_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, html.load_more_button))) 
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            tweets = soup.find_all('div', class_=html.tweet_container)
            for tweet in tweets:
                try:
                    username = tweet.find('a', class_=html.tweet_username).get_text() # Scrapped username
                    tweet_text = tweet.find('div', class_=html.tweet_text).get_text() # Scrapped tweet text
                    tweet_time = tweet.find('span', class_=html.tweet_time).find('a')['title'] # Scrapped time
                    
                    tweets_corpus.append(
                        {
                            'time':tweet_time,
                            'tweet':tweet_text,
                            'username':username
                        }
                    ) 
                
                except AttributeError: 
                    continue
                
            load_more_button.click()
            print(f"Tweets scraped: {len(tweets_corpus)}")
            
            if len(tweets_corpus) >= limit:
                print("=== done! ===")
                
                print(f"success scrapping {len(tweets_corpus)} tweets")
                break
    
    except Exception as _:
        print("Finished loading all content or an error occurred:", str(_))
        
    
    return tweets_corpus
