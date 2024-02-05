from time import sleep

from selenium.webdriver.common.by import By
from web_scraper import WebScraper

url = "https://www.gulfood.com/exhibitors"


def main():
    """
    Initialize the webscraping process.
    """
    # Initialize the WebScraper class.
    scraper = WebScraper()
    # Navigate to the URL.
    scraper.navigate_to_url(url)
    sleep(10)
    # Navigate to the next page.
    # scraper.navigate_to_next_page(locator_type="xpath", locator_value="/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/div[6]/div/ul/li[9]")
    # sleep(5)
    # Find the page number of the first page.
    first_page_n = int(
        scraper.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/div[6]/div/ul/li[1]/a",
        ).text
    )
    sleep(2)
    # Find the page number of the last page.
    total_pages = int(
        scraper.driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/div[6]/div/ul/li[8]/a",
        ).text
    )

    print(f"Total number of pages:\n{total_pages}\n------------------")

    # Get full list of exhibitors on the page.
    ul_element = scraper.driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div[2]/main/div[2]/div/div/div/article/div/div/div/div/div/ul[2]",
    )
    print(ul_element)
    item_elements = ul_element.find_elements(By.TAG_NAME, "li")
    # print(item_elements)
    # for item in item_elements:
    #     print(item.text)
    row = scraper.driver.find_elements(
        By.CLASS_NAME,
        "m-exhibitors-list__items__item m-exhibitors-list__items__item--status-mainexhibitor",
    )
    print(row)
    for item in row:
        # Find elements in the row.
        # Add your code here to process each item in the row.
        # Find the icon element.
        icon_element = item.find_element(
            By.CLASS_NAME, "m-exhibitors-list__items__item__logo"
        )
        icon_src = icon_element.get_attribute("src")
        print(icon_src)
    # question_list = []
    # for item in item_elements:
    #     question = {
    #         "icon": item.find_element(By.XPATH, "m-exhibitors-list__items__item__logo").get_attribute("src"),
    #     }
    #     question_list.append(question)

    scraper.quit()


if __name__ == "__main__":
    main()
    print("Done.")
