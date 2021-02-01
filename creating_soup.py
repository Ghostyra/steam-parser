import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Get all game-links from page
def get_links(url):
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    driver.get(url)

    len_page = len(driver.page_source)
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        new_len_page = len(driver.page_source)
        if new_len_page == len_page:
            break
        len_page = new_len_page

    links = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()

    div = soup.find("div", attrs={"id": "search_resultsRows"})
    for a in div.find_all("a"):
        link = a.get("href")
        # Verify that is no bundle
        if "/sub/" in link:
            continue
        links.append(link)

    with open("file.txt", "w") as f:
        for link in links:
            f.write(str(link) + "\n")

    return links


# Create soup for parsing
def create_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    return soup