from time import sleep

from web_scraper import WebScraper

url = "https://www.gulfood.com/exhibitors?&page=01"


def main():
    """
    Main function to run the extraction process.
    """
    scraper = WebScraper(headless=False)
    scraper.navigate_to_page(url)
    sleep(5)
    scraper.click_got_it_button()
    sleep(2)
    data = scraper.extract_table_data()
    print(data)
    df = scraper.data_to_dataframe(data)
    print(df.head())
    scraper.close_driver()


if __name__ == "__main__":
    main()
