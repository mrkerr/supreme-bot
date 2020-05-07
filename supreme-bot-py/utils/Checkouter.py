from constants.constants import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
class Checkouter():

  def __init__(self, driver):
    self.driver = driver

  def __click_checkout_button(self):
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
    for t in PersonalConstants.TEL:
      self.__text_input(tel_element, t)
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