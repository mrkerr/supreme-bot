from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from constants.constants import *
from utils.size_categories import *
class LinkIterator():
  def __init__(self, driver):
    self.driver = driver
    self.total_cost = 0
    self.items_to_buy = ItemsToBuy.items
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
    
  # def __get_item_color(self):
  #   try:
  #     return self.driver.find_element_by_xpath("//p[@itemprop='model']").get_attribute('textContent')
  #   except NoSuchElementException:
  #     return False

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

    #try small -> large -> medium
    try:
      return dropdown.find_element_by_xpath("//option[text()='Small']").click()
    except NoSuchElementException:
      try:
        return dropdown.find_element_by_xpath("//option[text()='Large']").click()
      except NoSuchElementException:   
        try:
          return dropdown.find_element_by_xpath("//option[text()='Medium']").click()
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
          return f'This item costs {cost} dollars. The total cost is now {self.total_cost} dollars'
        except StaleElementReferenceException:
          continue

    except NoSuchElementException:  
      return False

    def __check_was_added(self):
      while True:
        return self.driver.find_element_by_ta

  def iterate_links(self, item_links):

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

    num_items_added = 0
    max_items = len(self.items_to_buy)
    print('ITEM LINKS FOR CORRECT CATEGORIES BELOW')
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
        print('Attempting to buy ' + item_name)

        #check if we need to select size
        for c in self.size_categories:
          if c in link:
            self.__select_size()
            break
        print('Adding item to cart')
        add_to_cart = self.__click_add_to_cart()
      else:
        found_match = False
        for name in self.items_to_buy:
          if name == item_name:
            found_match = True
        if not found_match:
          print('Can not find ' + item_name + ' in ')
          print(self.items_to_buy)
          self.__remove_item_alternate_links()
        continue

      #print results if succesfully added to cart
      if add_to_cart:
        num_items_added += 1
        if num_items_added == max_items:
          break
        self.__remove_item_alternate_links()
        print('ADDED ' + item_name + ' TO CART SUCCESSFULLY\U0001f64f')
        print(add_to_cart + '\n')
      else:
        self.__remove_item_alternate_links()