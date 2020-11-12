import json
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from typing import List
import settings


class Reader:
    def __init__(self):
        self.all_items = []

    def get_all_items(self) -> List:
        """

        :return:
        """
        return self.all_items

    async def find_items(self) -> List:
        url_web = settings.URL_NARUSHITEL_KARATELI_WEB
        url_js = settings.URL_NARUSHITEL_KARATELI_XHR
        opts = webdriver.ChromeOptions()
        opts.add_argument("headless")
        browser = webdriver.Chrome(settings.PATH_CHROME_DRIVER, options=opts)
        browser.get(url_web)  # must fetch web first, otherwise it thinks CORS have been violated
        browser.get(url_js)

        # time.sleep(10)
        # wait = WebDriverWait(browser, 20)
        # wait.until(EC.visibility_of_all_elements_located)

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        json_text = soup.pre.text

        # here are ALL persons: punishers (karateli), falsifiers (falsifikatori) and servants (posobniki)
        self.all_items = json.loads(json_text)
        return self.all_items
