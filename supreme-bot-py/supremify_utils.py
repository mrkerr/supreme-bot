class LinkGetter():

  def __init__(self, driver):
    self.driver = driver

  #driver methods should be in while loop to keep checking in case there is a wait
  def __find_items_container(self):
    while True:
      try:
        return self.driver.find_element_by_id('container')
      except NoSuchElementException:
        continue

  def __find_list_elements(self, container_ul):
    return container_ul.find_elements_by_tag_name('li')

  def __find_item_link(self, list_element):
    sold_out = False
    try:
      sold_out = list_element.find_element_by_class_name('sold_out_tag')
    except NoSuchElementException:  
      sold_out = False

    if not sold_out:
      return list_element.find_element_by_tag_name('a').get_attribute('href')
    else:
      return False

  def get_links(self):
    container_ul = self.__find_items_container()
    list_elements = self.__find_list_elements(container_ul)

    links = []
    for le in list_elements:
      link = self.__find_item_link(le)
      if link:
        links.append(link)

    return links


from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from items_to_buy import *
class LinkIterator():
  def __init__(self, driver):
    self.driver = driver
    self.total_cost = 0
    self.items_to_buy_dict = ItemsToBuy.items
    self.items_to_buy = list(self.items_to_buy_dict.keys())
    self.removed_links = []
    self.size_categories = SizeCategories.size_categories

  def __open_item(self, link):
    print('visiting this link ' + link)
    self.driver.get(link)

  def __get_item_name(self):
    while True:
      try:
        return self.driver.find_element_by_xpath("//h2[@itemprop='name']").get_attribute('textContent')
      except NoSuchElementException:
        continue
    
  def __get_item_color(self):
    try:
      return self.driver.find_element_by_xpath("//p[@itemprop='model']").get_attribute('textContent')
    except NoSuchElementException:
      return False

  def __add_item_cost(self):
    while True:
      try:
        return self.driver.find_element_by_xpath("//span[@itemprop='price']").get_attribute('textContent')
      except NoSuchElementException:
        continue

  def __select_size(self):
    print('selecting size')
    dropdown = ''
    #find dropdown
    while True:
      try:
        dropdown = self.driver.find_element_by_xpath("//select[@name='s']")
        break
      except NoSuchElementException:
        continue

    #try large -> medium -> small
    try:
      return dropdown.find_element_by_xpath("//option[text()='Large']").click()
    except NoSuchElementException:
      try:
        return dropdown.find_element_by_xpath("//option[text()='Medium']").click()
      except NoSuchElementException:   
        try:
          return dropdown.find_element_by_xpath("//option[text()='Small']").click()
        except NoSuchElementException:
          return False


  def __remove_item_alternate_links(self):
    styles_list = False
    while True:
      try:
        styles_list = self.driver.find_element_by_class_name('styles').find_elements_by_tag_name('li')
      except NoSuchElementException:
        continue
      if styles_list:
        break

    for s in styles_list:
      self.removed_links.append('https://www.supremenewyork.com' + s.find_element_by_tag_name('button').get_attribute('data-url'))

  def __click_add_to_cart(self):
    try:
      self.driver.find_element_by_name('commit').click()
      cost = float(self.__add_item_cost()[1:])
      self.total_cost += cost

      #wait for the cart to actually add the item
      commit_button = False
      while True:
        try:
          commit_button = self.driver.find_element_by_name('commit')
          while(commit_button.get_attribute('value') == 'add to cart'):
            continue
          return f'This item costs {cost} dollars. The total cost of this tab is now {self.total_cost} dollars'
        except StaleElementReferenceException:
          continue

    except NoSuchElementException:  
      return False

    def __check_was_added(self):
      while True:
        return self.driver.find_element_by_ta

  def iterate_links(self, item_links, limit=10):

    #first, remove links for categories we don't want to visit
    categories = ItemsToBuy.items_categories
    num_categories = len(ItemsToBuy.items_categories)
    for l in item_links:
      cats_checked = 0
      for cat in categories:
        if cat not in l:
          cats_checked += 1
          if cats_checked >= num_categories:
            self.removed_links.append(l)
            break
        else:
          break
      
    print('Removed cateogry links: ')
    print(self.removed_links)
    print('\n')

    i = 0
    num_items_added = 0
    max_items = len(self.items_to_buy)
    print('ITEM LINKS BELOW')
    print(item_links)
    for link in item_links:
      #check we haven't removed this link
      if link in self.removed_links:
        continue

      #open link
      self.__open_item(link)

      #only add to cart once we've checked item is on the list
      add_to_cart = False
      item_name = self.__get_item_name().strip()

      if item_name in self.items_to_buy:
        print('Looking at ' + item_name)
        target_color = self.items_to_buy_dict[item_name].strip()
        if target_color != self.__get_item_color():
          print('not getting ' + item_name + ' ' + self.__get_item_color())
          continue
        #check if we need to select size
        for c in self.size_categories:
          if c in link:
            print('selecting size')
            self.__select_size()
            break
        print('Adding item to cart: ')
        print(item_name)
        add_to_cart = self.__click_add_to_cart()
      else:
        found_match = False
        for name in self.items_to_buy:
          if name == item_name:
            found_match = True
        if not found_match:
          print('Can not find ' + item_name + 'in ')
          print(self.items_to_buy)
          self.__remove_item_alternate_links()
        continue

      #print results if succesfully added to cart
      if add_to_cart:
        num_items_added += 1
        if num_items_added == max_items:
          break
        self.__remove_item_alternate_links()
        print('\n' + link + ' ADDED TO CART SUCCESSFULLY\U0001f64f')
        print(add_to_cart + '\n')
        i+=1
      else:
        self.__remove_item_alternate_links()
      if i == limit:
        break
    print(f'TOTAL COST FOR THIS TAB: {self.total_cost} dollars\n')
    print('FINAL REMOVED LIST: ')
    print(self.removed_links)
    print('\n')

from checkout_constants import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
class SupremeCheckouter():

  def __init__(self, driver):
    self.driver = driver

  def __click_checkout_button(self):
    print('got to checkout')
    self.driver.get('https://www.supremenewyork.com/checkout')
  
  def __text_input(self, element, text):
    element.send_keys(text)

  def __fill_in_personal(self):
    name_element = False
    while not name_element:
      try:
        name_element = self.driver.find_element_by_id('order_billing_name')
      except NoSuchElementException:
        continue
    email_element = self.driver.find_element_by_id('order_email')
    tel_element = self.driver.find_element_by_id('order_tel')
    address_element = self.driver.find_element_by_name('order[billing_address]')
    apt_element = self.driver.find_element_by_name('order[billing_address_2]')
    zip_element = self.driver.find_element_by_name('order[billing_zip]')
    city_element = self.driver.find_element_by_name('order[billing_city]')
    state_element = self.driver.find_element_by_xpath("//select[@id='order_billing_state']/option[text()='IL']")


    self.__text_input(name_element, PersonalConstants.NAME)
    self.__text_input(email_element, PersonalConstants.EMAIL)
    self.__text_input(tel_element, PersonalConstants.TEL)
    self.__text_input(address_element, PersonalConstants.ADDR)
    self.__text_input(apt_element, PersonalConstants.APT)
    self.__text_input(zip_element, PersonalConstants.ZIP)
    time.sleep(1)
    city_element.clear()
    self.__text_input(city_element, PersonalConstants.CITY)
    state_element.click()

  def __fill_in_card(self):
    number_element = self.driver.find_element_by_xpath("//input[@placeholder='number']")
    month_element = self.driver.find_element_by_xpath("//select[@id='credit_card_month']/option[text()=" + CardConstants.MON + "]")
    year_element = self.driver.find_element_by_xpath("//select[@id='credit_card_year']/option[text()=" + CardConstants.YER + "]")
    cvv_element = self.driver.find_element_by_xpath("//input[@placeholder='CVV']")

    self.__text_input(number_element, CardConstants.NUM)
    self.__text_input(cvv_element, CardConstants.CEV)
    month_element.click()
    year_element.click()

  def checkout(self):
    self.__click_checkout_button()
    self.__fill_in_personal()
    self.__fill_in_card()