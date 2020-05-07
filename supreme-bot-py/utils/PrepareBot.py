import time
from datetime import datetime, timedelta
from utils.Checkouter import *
from utils.LinkGetter import *
from utils.LinkIterator import *
from constants.constants import *
from selenium.common.exceptions import NoSuchElementException

class PrepareBot():

    def __init__(self, driver):
        self.driver = driver
        self.drop_time = DropInfo.DROP_TIME
        self.test_mode = DropInfo.TEST_MODE
        self.url = DropInfo.URL
        self.total_site_cost = 0

    def crawl(self):
        print('BEGINNING CRAWL')

        tic = time.perf_counter()
        
        link_getter = LinkGetter(self.driver)
        item_links = link_getter.get_links()

        link_iterator = LinkIterator(self.driver)
        link_iterator.iterate_links(item_links)
        self.total_site_cost += link_iterator.total_cost
        print(f"OVERALL TOTAL IS {self.total_site_cost}\n\n")

        if self.total_site_cost > 0:
            checkouter = Checkouter(self.driver)
            checkouter.checkout()

        toc = time.perf_counter()
        print(f"COMPLETED IN {toc - tic:0.4f} SECONDS")

    def __check_first_link(self):
        try:
            return self.driver.find_element_by_class_name('inner-article').find_element_by_tag_name('a').get_attribute('href')
        except NoSuchElementException:
            return False

    def __wait_for_drop_time(self):
        
        curr_time = datetime.now().strftime("%H:%M:%S")
        first_item = self.__check_first_link()
        new_first_link = first_item

        while(curr_time < self.drop_time):
            curr_time = datetime.now().strftime("%H:%M:%S")

        while(not self.test_mode and (not new_first_link or first_item == new_first_link)):
            self.driver.get(self.url)
            time.sleep(0.5)
            new_first_link = self.__check_first_link()
            print('first link is still')
            print(first_item)

    def get_and_wait(self):
        self.driver.get(self.url)
        self.__wait_for_drop_time()