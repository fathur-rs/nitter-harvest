from dataclasses import dataclass


@dataclass(frozen=True)
class HTML:
    load_more_button: str = "//div[@class='show-more']"
    
    search_field:str = "//input[@name='q']"
    search_button:str = "//button[@type='submit']"
    
    tweet_container:str = "timeline-item"
    tweet_text:str = "tweet-content"
    tweet_username:str = "username"
    tweet_time:str = "tweet-date"
