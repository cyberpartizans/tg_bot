import os
from mimetypes import MimeTypes
from typing import List, Dict, Optional, Union
from telethon import TelegramClient, types  # type: ignore
from .item_parser import ItemParser
import settings


class ListParser:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def download_media(self, item: types.Message) -> Optional[List]:
        """

        :param item:
        :return:
        """
        media_out = []
        # Функция download_media требует разделителя в конце пути к каталогу,
        # в противном случае она обрабатывает путь как файл!
        file_path = await self.client.download_media(
            item,
            settings.PATH_FILES_BLACK_BOOK_TMP.rstrip(os.path.sep) + os.path.sep)
        if not file_path:
            return media_out
        target_file_name = "%s--%s" % (item.id, os.path.basename(file_path))
        target_file_path = os.path.join(settings.PATH_FILES_BLACK_BOOK, target_file_name)
        # print("\n file path: %s target file path %s" % (file_path, target_file_path))
        size = os.path.getsize(file_path)
        os.rename(file_path, target_file_path)
        media_out.append({
            "file_name": target_file_name,
            "original_file_name": "",
            "external_id": "",
            "size": size,
            "type": MimeTypes().guess_type(target_file_name),
            "external_url": "",
        })
        return media_out

    async def parse_all_items_gen(self, items: List):
        """

        :param items:
        :param items:
        :return:
        """
        items_by_ext_id = {}
        items_grouped = {}

        for item in items:
            items_by_ext_id[item.id] = item
            if item.grouped_id:
                if item.grouped_id not in items_grouped:
                    items_grouped[item.grouped_id] = []
                items_grouped[item.grouped_id].append({
                    "external_id": item.id,
                    "grouped_id": item.grouped_id,
                    "files": [],
                })

        print("\nBlack Book of Belarus (Черная Книга Беларуси) - parsing items...")
        for item in items:
            msg_dict = item.to_dict()
            res: Optional[Dict] = await ItemParser(msg_dict).get_person_data()
            if not res:
                continue
            media_files = await self.download_media(item)
            if media_files:
                res["photos"].extend(media_files)

            if item.grouped_id and item.grouped_id in items_grouped:
                for g_item in items_grouped[item.grouped_id]:
                    if g_item["external_id"] == item.id:
                        continue
                    g_media_files = await self.download_media(items_by_ext_id[g_item["external_id"]])
                    if g_media_files:
                        res["photos"].extend(g_media_files)
            yield res
