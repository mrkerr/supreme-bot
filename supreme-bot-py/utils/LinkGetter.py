from selenium.common.exceptions import NoSuchElementException
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
