import sys

from app.web_scraper import WebScraper

print(f"Python interpreter path: {sys.executable}")
# sys.path.append('C:/Users/Felipe/python_work/Projects/webscraping-data-project')
# from app.datasource.web_scraper import WebScraper


url = "https://www.gulfood.com/exhibitors"


def main():
    """
    Initialize the webscraping process.
    """
    scraper = WebScraper()
    scraper.navigate_to_url(url)
    scraper.quit()


if __name__ == "__main__":
    main()
    print("Done.")
