from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .utils.webdriver import start_webdriver
from .utils.html_element import HTML

html = HTML()

def profile_tweets(username: str, limit: int = 100) -> list:
    """
    Scrape tweets from a user's profile on nitter.poast.org.

    This function uses Selenium WebDriver to navigate to a user's profile page on nitter.poast.org
    and scrape their tweets. It continuously loads more tweets until it reaches the specified limit
    or there are no more tweets to load.

    Args:
        username (str): The Twitter username of the profile to scrape (without the @ symbol).
        limit (int, optional): The maximum number of tweets to scrape. Defaults to 100.

    Returns:
        list[dict]: A list of dictionaries, each containing information about a single tweet.
                    Each dictionary has the following keys:
                    - 'time': The timestamp of the tweet (str)
                    - 'tweet': The text content of the tweet (str)

    Raises:
        Exception: If an error occurs during the scraping process. The error message is printed.

    Note:
        - This function requires a working internet connection.
        - The scraping process may take some time depending on the number of tweets requested.
        - The function uses Selenium WebDriver, which must be properly set up in the environment.
        - The HTML class from .utils.html_element is used for locating elements on the page.
    """
    
    driver = start_webdriver()
    driver.get(f'https://nitter.poast.org/{username}')
    print(f"=== Redirecting to {username}'s tweets profile ===")
    
    tweets_corpus = []
    
    try:
        while len(tweets_corpus) < limit:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, html.tweet_container))
            )
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            new_tweets = [
                {
                    'time': tweet.find('span', class_=html.tweet_time).find('a')['title'],
                    'tweet': tweet.find('div', class_=html.tweet_text).get_text(strip=True)
                }
                for tweet in soup.find_all('div', class_=html.tweet_container)
                if tweet.find('div', class_=html.tweet_text) and tweet.find('span', class_=html.tweet_time)
            ]
            
            tweets_corpus.extend(new_tweets)
            
            if len(tweets_corpus) >= limit:
                tweets_corpus = tweets_corpus[:limit]
                break
            
            try:
                load_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, html.load_more_button))
                )
                driver.execute_script("arguments[0].click();", load_more_button)
            except:
                break
            
            print(f"Tweets scraped: {len(tweets_corpus)}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()
    
    print("=== Done! ===")
    print(f"Successfully scraped {len(tweets_corpus)} tweets")
    return tweets_corpus