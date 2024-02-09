import os
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Initialize the webdriver
class WebScraper:
    def __init__(self, headless=False):
        self.driver = self.initialize_webdriver(headless)

    def initialize_webdriver(self, headless=False):
        """
        Initializes the webdriver with the specified options.
        - `headless`: `bool`, whether to run the browser in headless mode. Default is `False`.
        This is useful for running the scraper in a headless environment, such as a server.
        """
        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        return driver

    def navigate_to_page(self, url):
        """Navigates to the specified page and returns the current URL."""
        self.driver.get(url)
        return self.driver.current_url

    def click_got_it_button(self):
        """
        Clicks the "Got it" button if it exists. If it doesn't, continue with the process.
        """
        try:
            wait = WebDriverWait(self.driver, 10)  # Wait for 10 seconds.
            got_it_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc-btn.cc-dismiss"))
            )
            got_it_button.click()
        except TimeoutException:
            pass

    def extract_table_data(self):
        """
        Extracts the data from the table and returns a list of dictionaries.
        """
        try:
            wait = WebDriverWait(self.driver, 5)  # Wait for 10 seconds.
            table = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/ul[2]",
                    )
                )
            )
            rows = table.find_elements(By.TAG_NAME, "li")
        except NoSuchElementException:
            print("The table was not found.")
            return []

        data = []
        wait = WebDriverWait(self.driver, 5)  # Wait for 5 seconds.

        for row in rows:
            logo_url = row.find_element(
                By.CSS_SELECTOR, ".m-exhibitors-list__items__item__logo__link img"
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
            except NoSuchElementException:
                category_icon_url = None
            try:
                country_element = row.find_element(
                    By.XPATH,
                    ".//div[contains(@class, 'm-exhibitors-list__items__item__location')]",
                )
                country = country_element.text.strip()
            except NoSuchElementException:
                print("Country not found, waiting for 5 seconds")
                sleep(5)
                country = None

            row_data = {
                "logo_url": logo_url,
                "name": name,
                "hall": hall,
                "stand": stand,
                "category_icon_url": category_icon_url,
                "country": country,
            }
            data.append(row_data)

        return data

    def data_to_dataframe(self, data):
        """Converts the data to a pandas DataFrame."""
        df = pd.DataFrame(data)
        return df

    def export_to_csv(self, df, filename):
        """
        Exports the DataFrame to a CSV file. Define the filename without the extension.
        """
        df.to_csv(filename, index=False, header=True)

    def extract_total_pages(self):
        """
        Extracts the total number of pages from the pagination.
        """
        element = self.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/div[6]/div/ul/li[8]/a",
        )
        total_pages_text = element.text

        return int(total_pages_text)

    def close_driver(self):
        """Quits the webdriver."""
        self.driver.quit()
