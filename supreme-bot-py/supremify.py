from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from supremify_utils import *
from tab_constants import *
import time
from datetime import datetime, timedelta

BASE_URL = 'https://www.supremenewyork.com/shop/'
MAX_ITEMS_TO_VISIT_PER_TAB = 500
DROP_TIME = "19:44:00"
FIRST_PAGE = True

total_site_cost = 0
        
def crawl(driver, checkout_ready):
    print('BEGINNING CRAWL')
    global FIRST_PAGE
    global total_site_cost

    tic = time.perf_counter()
    FIRST_PAGE = False
    
    link_getter = LinkGetter(driver)
    item_links = link_getter.get_links()
    print('LinkGetter Links: ')
    print(item_links)
    print('\n')

    link_iterator = LinkIterator(driver)
    link_iterator.iterate_links(item_links, MAX_ITEMS_TO_VISIT_PER_TAB)
    total_site_cost += link_iterator.total_cost
    print(f"OVERALL TOTAL IS {total_site_cost}\n\n")

    if total_site_cost > 0 and checkout_ready:
        supreme_checkouter = SupremeCheckouter(driver)
        supreme_checkouter.checkout()

    toc = time.perf_counter()
    print(f"COMPLETED IN {toc - tic:0.4f} SECONDS")

def check_shop_live(driver):
    try:
        return driver.find_element_by_class_name('current')
    except NoSuchElementException:  
        return False

def wait_for_drop_time(driver, url):
    curr_time = datetime.now().strftime("%H:%M:%S")
    page_loaded = check_shop_live(driver)
    while(curr_time < DROP_TIME):
        curr_time = datetime.now().strftime("%H:%M:%S")
    while(not page_loaded):
        driver.get(url)
        sleep(1)
        page_loaded = check_shop_live(driver)
        print('Drop time has passed but shop not loaded')

def get_and_crawl(driver, url, checkout_ready):
    print('get_and_crawl')
    global FIRST_PAGE

    driver.get(url)
    if FIRST_PAGE:
        wait_for_drop_time(driver, url)
    crawl(driver, checkout_ready)

def iterate_through_tabs(driver):
    checkout_ready = False
    tab_links = TabConstants()
    i = 0

    for tl in tab_links.POSSIBLE_TABS:
        print(tl)
        if i == tab_links.LAST_TAB_INDEX:
            checkout_ready = True
        else:
            i+=1
        if tl[1]:
            if tl[0] == 'new' or tl[0] == 'all':
                get_and_crawl(driver, BASE_URL + tl[0], checkout_ready)
            else:
                get_and_crawl(driver, BASE_URL + 'all/' + tl[0], checkout_ready)
        if checkout_ready:
            break

def supremify():
    driver = webdriver.Firefox()
    iterate_through_tabs(driver)

    #TODO: Delete these lines before using irl
    time.sleep(20)
    driver.close()

supremify()