import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from typing import List
import settings
from constants import PersonType
from utils.text.text import clean_found_item


class Reader:
    def __init__(self):
        self.all_items = []

    def get_all_items(self) -> List:
        """

        :return:
        """
        return self.all_items

    # TODO - in progress
    async def get_person_details(self, url):
        url = 'https://bandaluki.info/bandits/shabunya-viktoryya-valeryevna/'
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        personal_data_out = {
            'features': [],
            'notes': [],
            'images': [],
        }
        personal_details = soup.find_all("div", attrs={"class": "project-info-box"})
        for detail in personal_details:
            feature = clean_found_item(detail.h4.get_text())
            feature_data = {
                'name': feature,
                'values': []
            }
            print(f"\n\n FEATURE: {feature}")
            for a_val in detail.div.children:
                if a_val.name == 'a':
                    print("\n ANCHOR ", a_val, a_val.name)
                    feature_data["values"].append((
                        a_val.get_text(),
                        a_val["href"]
                    ))
            personal_data_out["features"].append(feature_data)
            print("\n ==== feature data: ", feature_data)
        notes = soup.find("div", attrs={"class": "project-description post-content fusion-project-description-details"})

        notes_html_text = str(notes)
        print("\n\n NOTES HTML TEXT ", notes_html_text)
        images = notes.findChildren('img')

        paragraphs = notes.findChildren("p")

        strongs_out = []

        cur_strong_cont = None
        for par in paragraphs:
            if cur_strong_cont:
                strongs_out.append((cur_strong_cont, str(clean_found_item(par.get_text()))))
                cur_strong_cont = None

            strongs = par.findChildren("strong")
            print("\n PARAGRAPH: ", par, "\n")
            for i, strong in enumerate(strongs):
                strong_name = clean_found_item(strong.get_text())
                print("\n====   STRONG: ", strong, "name:", strong_name, "next sibling ", strong.next_sibling)
                # next sibling found and it is not a tag
                if strong.next_sibling and not re.match('<br.+?>', str(strong.next_sibling)):
                    strongs_out.append((strong_name, clean_found_item(str(strong.next_sibling))))
                elif strong.next_sibling and strong.next_sibling.next_sibling:
                    strongs_out.append((strong_name, clean_found_item(str(strong.next_sibling.next_sibling))))
                elif i + 1 >= len(strongs):
                    cur_strong_cont = strong_name

        print("\n STRONGS OUT ", strongs_out)

        for img in images:
            personal_data_out["images"].append((
                img["src"],
                img["srcset"]
            ))

        # print("\n\n NOTES ", notes)
        # print("\n IMAGES ", images)
        personal_data_out["notes"] = [i for i in notes.findChildren("p")]
        # print("\n PERSONAL DATA OUT ", personal_data_out)
        quit()


    async def find_items(self) -> List:
        url_person_page_tpl = settings.URL_BANDA_LUKI_WEB_PERSON_PAGE_TPL

        categories_bl = [
            ['sudyi', 'Судьи', PersonType.JUDGE],
            ['siloviki', 'Силовики', PersonType.PUNISHER],
            ['propagandist', 'Пропагандисты', PersonType.PROPAGANDIST],
            ['chinovniki', 'Чиновники', PersonType.OFFICIAL],
            ['prochie', 'Прочие', PersonType.OTHER]
        ]

        opts = webdriver.ChromeOptions()
        opts.add_argument("headless")
        self.browser = webdriver.Chrome(settings.PATH_CHROME_DRIVER, options=opts)

        all_items = []
        page_items = []

        for category in categories_bl:
            print("\n CATEGORYYYYYYYY:  ", category[0])
            page = 1
            last_page_items = []
            while True:
                page_items = []
                if page < 2:
                    url = settings.URL_BANDA_LUKI_CATEGORY_LIST_TPL % category[0]
                else:
                    url = settings.URL_BANDA_LUKI_CATEGORY_LIST_PAGES_TPL % (category[0], page)
                self.browser.get(url)
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                # <h2 class="entry-title fusion-post-title"><a href="/bandits/aleksa-aleksandr-i/">Алёкса Александр И.</a></h2>
                h2_list = soup.find_all("h2", attrs={"class": "entry-title fusion-post-title"})
                print("\n H2 list", h2_list)
                for h2_tag in h2_list:
                    person_url = "%s/%s" % (settings.URL_BANDA_LUKI_WEB_MAIN.rstrip("/"), h2_tag.a["href"].lstrip("/"))
                    full_name = h2_tag.a.get_text()
                    page_items.append({
                        'url': person_url,
                        'full_name': full_name,
                        'person_type': category[2],
                        'details': {}
                    })
                    print("\n full_name ", full_name)
                    person_details = await self.get_person_details(person_url)
                print("\n PAGE NO %d,  ITEMS: " % page, page_items, "PAGE URL ", url)

                all_items.extend(page_items)
                if not page_items or page_items == last_page_items:
                    print("\n LAST PAGE FOUND, BREAKING")
                    break
                last_page_items = page_items
                page += 1

        print("\n\n ALL ITEMS ", all_items)
        return self.all_items
