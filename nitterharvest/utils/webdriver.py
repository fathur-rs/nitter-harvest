from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def webdriver_options() -> Options:
    options = Options()
    options.add_argument("--headless")
    
    return options

def start_webdriver() -> webdriver:
    driver = webdriver.Firefox(options=webdriver_options())
    print("=== webdriver init ===")
    return driver