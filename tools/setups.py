from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_local_safe_setup():
    options = ChromeOptions() 
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    driver = Chrome(desired_capabilities = options.to_capabilities())

    return driver

def get_safe_setup():
    options = ChromeOptions() 
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    driver = webdriver.Remote("http://localhost:4444", desired_capabilities = options.to_capabilities())

    return driver