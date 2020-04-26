class LinkGetter():

  def __init__(self, driver):
    self.driver = driver

  def __find_items_container(self):
    return self.driver.find_element_by_id('container')

  def __find_list_elements(self, container_ul):
    return container_ul.find_elements_by_tag_name('li')

  def __find_item_link(self, list_element):
    return list_element.find_element_by_tag_name('a').get_attribute('href')

  def get_links(self):
    container_ul = self.__find_items_container()
    list_elements = self.__find_list_elements(container_ul)

    links = []
    for le in list_elements:
      links.append(self.__find_item_link(le))

    return links


from selenium.common.exceptions import NoSuchElementException
class LinkIterator():
  def __init__(self, driver):
    self.driver = driver
    self.total_cost = 0

  def __open_item(self, link):
    self.driver.get(link)

  def __add_item_cost(self):
    return self.driver.find_element_by_xpath("//span[@itemprop='price']").get_attribute('textContent')
  
  def __click_add_to_cart(self):
    try:
      self.driver.find_element_by_name('commit').click()
      cost = float(self.__add_item_cost()[1:])
      self.total_cost += cost
      return f'This item costs {cost} dollars. The total cost of this tab is now {self.total_cost} dollars'

    except NoSuchElementException:  
      return False

  def iterate_links(self, item_links, limit=10):
    i = 1
    for link in item_links:
      self.__open_item(link)
      add_to_cart = self.__click_add_to_cart()
      if add_to_cart:
        print('\n' + link + ' ADDED TO CART SUCCESSFULLY\U0001f64f')
        print(add_to_cart + '\n')
      else:
        print(link + ' IS SOLD OUT\U0001f44e\n')
      i+=1
      if i == limit:
        break
    print(f'TOTAL COST FOR THIS TAB: {self.total_cost} dollars')

from checkout_constants import *
class SupremeCheckouter():

  def __init__(self, driver):
    self.driver = driver

  def __click_checkout_button(self):
    self.driver.get('https://www.supremenewyork.com/checkout')
  
  def __text_input(self, element, text):
    element.send_keys(text)

  def __fill_in_personal(self):
    name_element = self.driver.find_element_by_id('order_billing_name')
    email_element = self.driver.find_element_by_id('order_email')
    tel_element = self.driver.find_element_by_id('order_tel')
    address_element = self.driver.find_element_by_name('order[billing_address]')
    apt_element = self.driver.find_element_by_name('order[billing_address_2]')
    zip_element = self.driver.find_element_by_name('order[billing_zip]')
    city_element = self.driver.find_element_by_name('order[billing_city]')

    self.__text_input(name_element, PersonalConstants.NAME)
    self.__text_input(email_element, PersonalConstants.EMAIL)
    self.__text_input(tel_element, PersonalConstants.TEL)
    self.__text_input(address_element, PersonalConstants.ADDR)
    self.__text_input(apt_element, PersonalConstants.APT)
    self.__text_input(zip_element, PersonalConstants.ZIP)
    self.__text_input(city_element, PersonalConstants.CITY)

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