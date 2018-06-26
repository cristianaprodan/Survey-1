from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)

    def wait_until_element_is_visible(self, element):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
        return  self.driver.find_element(element[0], element[1])

    def save_screenshot(self, location):
        self.driver.get_screenshot_as_file(location)