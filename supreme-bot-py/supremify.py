from selenium import webdriver
from utils.PrepareBot import *

def supremify():
    driver = webdriver.Firefox()
    bot = PrepareBot(driver)
    bot.get_and_wait()
    bot.crawl()

if __name__ == "__main__":
    supremify()