import concurrent.futures
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Initialize the WebScraper class.
class WebScraper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.driver = webdriver.Chrome()
        return cls._instance

    def navigate_to_url(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def scrape_page(self, url):
        self.navigate_to_url(url)
        scraper = WebScraper()
        wait = WebDriverWait(scraper.driver, 5)
        scraper.navigate_to_url(url)
        try:
            got_it_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/a"))
            )
            got_it_button.click()
        except NoSuchElementException:
            pass

        while True:
            data = []

            table = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/ul[2]",
                    )
                )
            )
            rows = table.find_elements(By.TAG_NAME, "li")

            for i in range(len(rows)):
                try:
                    # Re-find the row element before interacting with it
                    row = table.find_elements(By.TAG_NAME, "li")[i]
                    logo_url = row.find_element(
                        By.CSS_SELECTOR,
                        ".m-exhibitors-list__items__item__logo__link img",
                    ).get_attribute("src")
                    name = row.find_element(
                        By.CSS_SELECTOR,
                        ".m-exhibitors-list__items__item__name .m-exhibitors-list__items__item__name__link",
                    ).text.strip()
                    hall = row.find_element(
                        By.CSS_SELECTOR, ".m-exhibitors-list__items__item__hall"
                    ).text.strip()
                    stand = row.find_element(
                        By.CSS_SELECTOR, ".m-exhibitors-list__items__item__stand"
                    ).text.strip()
                    try:
                        category_icon_url = row.find_element(
                            By.CSS_SELECTOR,
                            ".m-exhibitors-list__items__item__category img",
                        ).get_attribute("src")
                    except:
                        category_icon_url = None
                    country = row.find_element(
                        By.CSS_SELECTOR, ".m-exhibitors-list__items__item__location"
                    ).text.strip()

                    row_data = {
                        "logo_url": logo_url,
                        "name": name,
                        "hall": hall,
                        "stand": stand,
                        "category_icon_url": category_icon_url,
                        "country": country,
                    }
                    data.append(row_data)
                except StaleElementReferenceException:
                    continue

            scraper.change_page()

            if not scraper.change_page():
                break
        next_url = self.change_page()
        return data, next_url

    def change_page(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            next_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".pagination__list__item__link.pagination__list__item__link--next",
                    )
                )
            )
            next_button.click()
            return True
        except NoSuchElementException:
            return False

    print("Done.")
