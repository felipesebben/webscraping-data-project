from time import sleep

import pandas as pd
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from app.web_scraper import WebScraper


@pytest.fixture
def scraper():
    """
    Fixture to initialize the scraper.
    """
    options = Options()
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )  # Disable logging
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    scraper = WebScraper(driver)
    yield scraper

    # Teardown
    scraper.driver.quit()


def test_navigate_to_page(scraper):
    """
    Test to navigate to a page.
    """
    url = "https://www.gulfood.com/exhibitors?&page=01"
    scraper.navigate_to_page(url)
    assert scraper.driver.current_url == url


def test_button_click(scraper):
    """
    Test to click the "Got it" button.
    """
    url = "https://www.gulfood.com/exhibitors?&page=01"
    scraper.navigate_to_page(url)
    got_it_button = scraper.driver.find_element(By.XPATH, "/html/body/div[1]/div/a")
    got_it_button.click()
    sleep(2)
    assert got_it_button is not None


def test_extract_table_data(scraper):
    """
    Test to extract the data from the table.
    """
    scraper.navigate_to_page("https://www.gulfood.com/exhibitors?&page=01")
    data = scraper.extract_table_data()
    assert isinstance(data, list)
    if data:
        assert isinstance(data[0], dict)


def test_data_to_dataframe(scraper):
    """
    Test to convert the data to a dataframe, if the data exists.
    """
    scraper.navigate_to_page("https://www.gulfood.com/exhibitors?&page=01")
    data = scraper.extract_table_data()
    df = scraper.data_to_dataframe(data)
    if data:
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == len(data)
    else:
        assert df is None
