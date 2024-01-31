from selenium import webdriver
from time import sleep
import pytest

from selenium.webdriver.common.by import By
import os
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class WebScraper:
    """
    Class to initialize the webscraper.
    """

    def __init__(self, headless=True, page_load_timeout=15):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_page_load_timeout(page_load_timeout)

    def navigate_to_url(self, url):
        self.driver.get(url)
        return self.driver.current_url

    def quit(self):
        self.driver.quit()

    def navigate_to_url(self, url):
        """
        Method to navigate to a URL.
        """
        self.driver.get(url)
        return self.driver.current_url
