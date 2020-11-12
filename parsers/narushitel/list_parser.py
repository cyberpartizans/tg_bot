import os
import requests
from typing import List, Dict, Optional
from .item_parser import ItemParser
from utils.text.text import narushitel_url_into_path
import settings


class ListParser:
    def __init__(self) -> None:
        res = requests.get(settings.URL_NARUSHITEL_MAIN)
        self.cookies = None

    def _get_cookies(self):
        if not self.cookies:
            res = requests.get(settings.URL_NARUSHITEL_MAIN)
            self.cookies = res.cookies
        return self.cookies

    async def download_media(self, item: Dict) -> List:
        """

        :param item:
        :return:
        """
        media_out = []
        # return []
        # бывают элементы, для которых вообще не определено поле "Attachments"
        if "Attachments" not in item["fields"] or not item["fields"]["Attachments"]:
            return media_out

        for att_item in item["fields"]['Attachments']:
            file_url = settings.URL_NARUSHITEL_MAIN.rstrip('/') + '/' + att_item["url"].lstrip('/')
            res = requests.get(file_url, cookies=self._get_cookies())
            if res.status_code != 200:  # нам не нужны поврежденные файлы!
                continue

            target_file_name = narushitel_url_into_path(att_item["url"], att_item['id'])
            media_out.append({
                "original_file_name": att_item["filename"],
                "file_name": target_file_name,
                "external_id": att_item["id"],
                "size": att_item["size"],
                "type": att_item["type"],
                "external_url": att_item["url"],
            })

            target_path_file = os.path.join(
                settings.PATH_FILES_NARUSHITEL,
                target_file_name
                )
            target_path_dir = os.path.dirname(target_path_file)
            print("\n\ntarget path file", target_path_file, "target_path_dir", target_path_dir, "id ", att_item['id'])

            if not os.path.exists(target_path_dir):
                os.makedirs(target_path_dir, 0o777, exist_ok=True)
            with open(target_path_file, "wb") as f:
                f.write(res.content)
                f.close()
        return media_out

    async def parse_all_items_gen(self, items: List):
        """

        :param items:
        :return:
        """
        print("\nNarushitel.org - parsing items...")
        for item in items:
            res: Optional[Dict] = await ItemParser(item).get_person_data()
            if res:
                photos_list = await self.download_media(item)
                res["photos"].extend(photos_list)
                yield res
        print("\nNarushitel.org - parsing of items is FINISHED.")

