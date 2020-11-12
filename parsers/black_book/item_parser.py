import re
from typing import List, Dict, Optional, Union
from utils.text.lexers.date import find_date_in_text, possible_adult_person_dob
from utils.text.lexers.person import is_person_by_full_name
from utils.text.lexers.personal_data_updater import update_person_data_using_lexers
from utils.text.text import clean_str
from parsers.item_parser_top import ItemParserTop


class ItemParser(ItemParserTop):
    def __init__(self, item: Dict):
        super().__init__(item)
        self.is_message = True if item and "message" in self.item and self.item["message"] else False
        self.date_of_birth_orig_text = ""
        self.person_data.update({
            "item_date": item["date"],
            "grouped_id": item["grouped_id"] if "grouped_id" in item and item["grouped_id"] else None,
            "is_person": False,
        })

    async def get_person_data(self) -> Optional[Dict]:
        """

        :return:
        """
        if not self.is_message:
            return None

        blocks = re.split("\n\n", self.item["message"])
        self.update_full_name(blocks[0])
        self.update_split_names()
        self.person_data["is_person"] = is_person_by_full_name(self.person_data["full_name"])
        if not self.person_data["is_person"]:
            return None
        block_indexes_used = [0]  # full_name/is_person
        # we must include block 0 as well, because sometimes date of birth or role is there
        for i, block in enumerate(blocks):
            block_used = self.update_date_of_birth(block) | \
                         self.update_desc_data(block) | \
                         self.update_phones(block) | \
                         self.update_social_fbs(block) | \
                         self.update_social_vks(block) | \
                         self.update_social_oks(block) | \
                         self.update_social_instagrams(block) | \
                         self.update_social_telegrams(block) | \
                         self.update_tags(block)
            if block_used:
                block_indexes_used.append(i)

        self.update_notes(blocks, block_indexes_used)
        return self.person_data

    def update_full_name(self, block: str):
        self.person_data["full_name"] = self.find_full_name(block)
        self.update_split_names()

    def find_full_name(self, block: str) -> str:
        """

        :param block:
        :return:
        """
        test_name = re.search(r"(.+)", block)  # until the first \n
        if test_name:
            return test_name.groups()[0]
        return ""

    def update_desc_data(self, block: str) -> bool:
        """

        :param block:
        :return:
        """
        update_person_data_using_lexers(block, self.person_data)
        return False

    # TODO: fetch roles from notes; it requires to have some dictionary of words
    #  like полковник, руководитель etc.
    #  With roles we'll be able to determine types as well (eg. punisher, regime's accomplice, judge etc)
    def update_notes(self, blocks: List, block_indexes_used: List) -> bool:
        """

        :param blocks:
        :param block_indexes_used:
        :return:
        """
        notes = []
        block_0 = blocks[0]
        block_0 = block_0.strip()
        full_name = self.find_full_name(blocks[0])
        block_0 = block_0.replace(full_name, "").strip()
        if self.date_of_birth_orig_text:
            block_0 = block_0.replace(self.date_of_birth_orig_text, "").strip()

        if block_0:  # if something is left in the block_0 after removal of name and date
            notes.append(block_0)

        for i, block in enumerate(blocks[1:]):
            j = i + 1
            if j in block_indexes_used:
                continue
            if re.search("Если вы были свидетелем", block, re.I):
                continue
            notes.append(block.strip())
        if notes:
            self.person_data["notes"].extend(notes)
            return True
        return False

    def update_tags(self, block: str) -> bool:
        """

        :param block:
        :return:
        """
        res = [clean_str(i) for i in re.findall(r"#[\w0-9\_]+", block)]
        if res:
            self.person_data["tags"].extend(res)
            return True
        return False

    def update_date_of_birth(self, block: str) -> bool:
        """

        :param block:
        :return:
        """
        if self.person_data["date_of_birth"]:
            return False

        dob_dt, dob_txt = find_date_in_text(block)
        if dob_dt and possible_adult_person_dob(dob_dt):
            self.person_data["date_of_birth"] = dob_dt
            self.date_of_birth_orig_text = dob_txt
            return True
        return False
