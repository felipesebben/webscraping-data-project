from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    """
    Fixture to initialize the browser.
    """
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver

    # Teardown
    driver.quit()


def test_navigate_to_page(browser):
    """
    Test to navigate to a page.
    """
    url = "https://www.gulfood.com/exhibitors?&page=01"
    browser.get(url)
    assert browser.current_url == url


def test_button_click(browser):
    """
    Test to click the "Got it" button.
    """
    url = "https://www.gulfood.com/exhibitors?&page=01"
    browser.get(url)
    got_it_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/a")
    got_it_button.click()
    sleep(2)
    assert got_it_button is not None


# def test_extract_data(browser):
#     element = browser.find_element(
#         By.CSS_SELECTOR, "pagination__list__item__link is-active"
#     )
#     assert element is not None
