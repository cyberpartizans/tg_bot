from typing import List, Dict, Optional
from utils.text.lexers.data.phrases import base_lexer_phrases
from utils.text.lexers.phone import find_phone_numbers
from utils.text.lexers.social import find_vks_in_text, find_oks_in_text, find_fbs_in_text, \
    find_instagrams_in_text, find_telegrams_in_text
from utils.text.lexers.person import split_full_name
from utils.text.easy_dict import get_phone_dict


class ItemParserTop:
    def __init__(self, item: Dict):
        """

        :param item:
        """
        self.item = item
        self.person_data = {
            "external_id": item["id"],
            "item_date": None,
            # поля дляnarushitel.org:
            "cities": [],
            # поля существующие также в black_book:
            "is_person": True,
            "source_id": None,  # TODO - зачем нам эта таблица? Пусть решим это.

            # TODO - пусть найдем лексер, чтобы правильного разделить полные имена и пол
            "full_name": "",
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "gender": None,
            # /TODO - пусть найдем лексер, чтобы правильного разделить полные имена и пол

            "origin_place": "",  # TODO - сейчас нет возможности получить эту информацию
            "identity_number": "",  # TODO - нам нужен "личный номер", если это не номер телефона (иногда это случается)
            "passport_number": "",  # TODO - надо проверить описания документов и найти лексер
            "passport_issue_date": None,  # TODO - очень сложно, хотя иногда возможно получить эту информацию
            "passport_issue_place": "",  # TODO - очень сложно, хотя иногда возможно получить эту информацию
            "rank": "",

            "birth_date": None,
            "date_of_birth": None,
            "notes": [],  # here are some social site links as well, TO BE PARSED TODO
            "roles": [],
            "types": [],
            "title": "",

            "phones": [],
            "addresses": [],
            'cars': [],
            "documents": [],
            "family_members": [],

            "social_fbs": [],
            "social_vks": [],
            "social_oks": [],
            "social_instagrams": [],
            "social_telegrams": [],

            "photos": [],
            "tags": [],
            "emails": [],
        }

    def update_split_names(self) -> None:
        if not self.person_data["full_name"]:
            return
        name_dict = split_full_name(self.person_data["full_name"])
        self.person_data["first_name"] = name_dict["first_name"]
        self.person_data["middle_name"] = name_dict["middle_name"]
        self.person_data["last_name"] = name_dict["last_name"]

    def update_phones(self, block: str) -> bool:
        """

        :param block:
        :return:
        """
        phones = find_phone_numbers(block)
        if phones:
            for i in phones:
                phone_dict = get_phone_dict(number=i)
                self.person_data["phones"].append(phone_dict)
            return True
        return False

    def update_social_vks(self, text: str) -> bool:
        """

        :param text:
        :return:
        """
        res = find_vks_in_text(text)
        self.person_data['social_vks'].extend(res)
        return True if res else False

    def update_social_fbs(self, text: str) -> bool:
        """

        :param text:
        :return:
        """
        res = find_fbs_in_text(text)
        self.person_data['social_fbs'].extend(res)
        return True if res else False

    def update_social_instagrams(self, text: str) -> bool:
        """

        :param text:
        :return:
        """
        res = find_instagrams_in_text(text)
        self.person_data['social_instagrams'].extend(res)
        return True if res else False

    def update_social_oks(self, text: str) -> bool:
        """

        :param text:
        :return:
        """
        res = find_oks_in_text(text)
        self.person_data['social_oks'].extend(res)
        return True if res else False

    def update_social_telegrams(self, text: str) -> bool:
        """

        :param text:
        :return:
        """
        res = find_telegrams_in_text(text)
        self.person_data['social_telegrams'].extend(res)
        return True if res else False

    # -- methods to override in children classes, kept for the sake of brevity (aka "interface") :
    async def get_person_data(self) -> Optional[Dict]:
        # override in children
        pass

    def update_addresses(self, *args, **kwargs):
        # override in children
        pass

    def update_cars(self, *args, **kwargs):
        # override in children
        pass

    def update_documents(self, *args, **kwargs):
        # override in children
        pass

    def update_family_members(self, *args, **kwargs):
        # override in children
        pass

    def update_photos(self, *args, **kwargs):
        # override in children
        pass

    def update_tags(self, *args, **kwargs):
        # override in children
        pass

    def update_emails(self, *args, **kwargs):
        # override in children
        pass

    def update_cities(self, *args, **kwargs):
        # override in children
        pass

    def update_full_name(self, *args, **kwargs):
        # override in children
        pass

    def update_types(self, *args, **kwargs):  # 1 or more possible
        # override in children
        pass

    def update_title(self, *args, **kwargs):
        # override in children
        pass

    def update_notes(self, *args, **kwargs):
        # override in children
        pass

    def update_date_of_birth(self, *args, **kwargs):
        # override in children
        pass

    def update_roles(self, *args, **kwargs):
        # override in children
        pass
