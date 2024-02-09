from time import sleep

from web_scraper import WebScraper


def main():
    """
    Main function to run the extraction process.
    """
    # Create a new instance of the WebScraper class
    scraper = WebScraper(headless=True)
    # Navigate to the page
    scraper.navigate_to_page("https://www.gulfood.com/exhibitors?&page=01")
    sleep(5)
    # # Click the "Got it" button
    scraper.click_got_it_button()
    # sleep(2)

    # Get the total number of pages to iterate over
    total_pages = scraper.extract_total_pages()

    # Iterate over each page
    for page_number in range(1, total_pages + 1):
        url = f"https://www.gulfood.com/exhibitors?&page={page_number:02d}"

        scraper.navigate_to_page(url)
        sleep(2)
        scraper.click_got_it_button()
        sleep(2)
        data = scraper.extract_table_data()
        df = scraper.data_to_dataframe(data)
        print(df.head())
        filename = f"data/raw/gulfood_exhibitors_page_{page_number:02d}.csv"
        scraper.export_to_csv(df, filename)

    scraper.close_driver()


if __name__ == "__main__":
    main()
