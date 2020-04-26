from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from supremify_utils import *
from tab_constants import *
import time
from datetime import datetime, timedelta

BASE_URL = 'https://www.supremenewyork.com/shop/'
MAX_ITEMS_TO_VISIT_PER_TAB = 5
DROP_TIME = "13:06:01"
FIRST_PAGE = True

total_site_cost = 0


def crawl(driver, checkout_ready):
    global FIRST_PAGE
    if FIRST_PAGE:
        curr_time = datetime.now().strftime("%H:%M:%S")
        while(curr_time < DROP_TIME):
            curr_time = datetime.now().strftime("%H:%M:%S")

        driver.refresh()
    FIRST_PAGE = False

    global total_site_cost
    
    link_getter = LinkGetter(driver)
    item_links = link_getter.get_links()

    link_iterator = LinkIterator(driver)
    link_iterator.iterate_links(item_links, MAX_ITEMS_TO_VISIT_PER_TAB)
    total_site_cost += link_iterator.total_cost
    print(f"OVERALL TOTAL IS {total_site_cost}\n\n")

    if total_site_cost > 0 and checkout_ready:
        supreme_checkouter = SupremeCheckouter(driver)
        supreme_checkouter.checkout()


def supremify():
    tic = time.perf_counter()
    driver = webdriver.Firefox()

    checkout_ready = False
    tab_links = TabConstants()
    i = 0
    for tl in tab_links.POSSIBLE_TABS:
        if i == tab_links.LAST_TAB_INDEX:
            checkout_ready = True
        else:
            i+=1
        if tl[1]:
            if tl[0] == 'new':
                driver.get(BASE_URL + tl[0])
                crawl(driver, checkout_ready)
            if tl[0] == 'all':
                driver.get(BASE_URL + tl[0])
                crawl(driver, checkout_ready)
            else:
                driver.get(BASE_URL + 'all/' + tl[0])
                crawl(driver, checkout_ready)

    toc = time.perf_counter()
    print(f"COMPLETED IN {toc - tic:0.4f} SECONDS")

    #TODO: Delete this line before using irl
    time.sleep(20)

    driver.close()

supremify()