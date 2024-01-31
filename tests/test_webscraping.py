from app.datasource.web_scraper import WebScraper
import pytest


@pytest.fixture
def scraper():
    """
    Create a WebScraper instance.
    """
    s = WebScraper()
    yield s
    s.quit()


def test_init():
    """
    Test that the WebScraper class is initialized correctly.
    """
    scraper = WebScraper(headless=False)
    assert scraper.driver is not None
    assert scraper.driver.current_url == "about:blank"
    scraper.quit()


def test_webscraper_initialization(scraper):
    """
    Test that the WebScraper class is initialized correctly.
    """
    assert isinstance(scraper, WebScraper)


def test_navigate_to_url(scraper):
    """
    Test that the WebScraper can navigate to a URL.
    """
    url = "https://www.google.com/"
    result = scraper.navigate_to_url(url)
    assert result == url


def test_quit():
    scraper.quit()
    with pytest.raises(Exception):
        # Attempting to use the driver after quitting should raise an exception
        scraper.driver.get("http://example.com/")
