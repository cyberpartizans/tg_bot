from telethon import TelegramClient  # type: ignore
from telethon.tl.functions.messages import GetHistoryRequest  # type: ignore
from typing import List


class Reader:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.offset_id = 0
        self.limit = 100
        self.all_items: List = []
        self.total_messages = 0
        self.total_count_limit = 0

    def get_all_items(self) -> List:
        """

        :return:
        """
        return self.all_items

    async def find_items(self) -> List:
        """

        :return:
        """
        black_book = await self.client.get_entity("t.me/BlackBookBelarus")
        while True:
            print("Current Offset ID is:", self.offset_id, "; Total Messages:", self.total_messages)
            history = await self.client(GetHistoryRequest(
                peer=black_book,
                offset_id=self.offset_id,
                offset_date=None,
                add_offset=0,
                limit=self.limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            print(f"Add new messages with len = {len(messages)}")
            for message in messages:
                self.all_items.append(message)
            self.offset_id = messages[len(messages) - 1].id
            self.total_messages = len(self.all_items)
        return self.all_items
