import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_links(url):
    driver = webdriver.Chrome()
    driver.get(url)

    len_page = len(driver.page_source)
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        new_len_page = len(driver.page_source)
        if new_len_page == len_page:
            break
        len_page = new_len_page

    links = []
    soup = BeautifulSoup(driver.page_source, "html.parser")

    div = soup.find("div", attrs={"id": "search_resultsRows"})
    for a in div.find_all("a"):
        links.append(a.get("href"))

    with open("file.txt", "w") as f:
        for link in links:
            f.write(str(link) + "\n")

    return links


def create_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    return soup