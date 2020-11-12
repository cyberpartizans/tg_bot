from typing import List, Dict, Optional, Union
from utils.text.lexers.address import extract_geoloc_and_address
from utils.text.lexers.personal_data_updater import update_person_data_using_lexers
from utils.text.text import date_from_text_to_obj, iso_date_to_obj
from utils.text.easy_dict import get_address_dict, get_job_dict
from constants import AddressType, get_person_type_for_ru_name
from parsers.item_parser_top import ItemParserTop
from .lexer_phrases import phrases


class ItemParser(ItemParserTop):
    def __init__(self, item: Dict):
        super().__init__(item)
        """

        :param item:
        """
        self.item = item
        self.date_of_birth_orig_text = ""

        self.person_data.update({
            "item_date": iso_date_to_obj(item["createdTime"]),
            # fields added for narushitel.org:
            "is_person": True,
        })
        print("\n Narushitel item id: %s Item date: %s " %
              (self.person_data["external_id"], self.person_data["item_date"]))

    async def get_person_data(self) -> Optional[Dict]:
        """

        :return:
        """
        self.update_cities()
        self.update_full_name()
        self.update_types()
        self.update_notes()
        self.update_date_of_birth()
        self.update_roles_and_title()
        self.update_phones_phone_field()
        self.update_addresses()

        if 'Notes' in self.item["fields"] and self.item["fields"]['Notes']:
            self.update_social_fbs(self.item["fields"]['Notes'])
            self.update_social_oks(self.item["fields"]['Notes'])
            self.update_social_vks(self.item["fields"]['Notes'])
            self.update_social_instagrams(self.item["fields"]['Notes'])
            self.update_social_telegrams(self.item["fields"]['Notes'])
            update_person_data_using_lexers(self.item["fields"]['Notes'], self.person_data, phrases)
            self.update_phones(self.item["fields"]['Notes'])

        return self.person_data

    def update_cities(self):
        self.person_data["cities"] = self.item['fields']['City'] if 'City' in self.item['fields'] else ""

    def update_full_name(self):
        self.person_data["full_name"] = self.item['fields']['Name'] if 'Name' in self.item['fields'] else ""
        self.update_split_names()

    def update_types(self):  # 1 or more possible
        if 'Type' in self.item['fields'] and self.item['fields']['Type']:
            for p_type_ru_name in self.item["fields"]["Type"]:
                p_type = get_person_type_for_ru_name(p_type_ru_name)
                if p_type:
                    self.person_data["types"].append(p_type)

    def update_notes(self):
        self.person_data["notes"] = self.item['fields']['Notes'] if 'Notes' in self.item['fields'] else ""

    def update_date_of_birth(self):
        date_text = self.item['fields']['DOB'] if 'DOB' in self.item['fields'] else None
        self.person_data["date_of_birth"] = date_from_text_to_obj(date_text)

    def update_roles_and_title(self):
        if 'Title' in self.item['fields'] and self.item['fields']['Title']:
            self.person_data["title"] = self.item['fields']['Title']
            self.person_data["roles"].append(get_job_dict(position=self.item['fields']['Title']))
        elif self.person_data["roles"]:  # например благодаря функции update_person_data_using_lexers
            self.person_data["title"] = self.person_data["roles"][0]['position']

    def update_phones_phone_field(self):
        if "Phone" in self.item["fields"] and \
                self.item["fields"]["Phone"] and \
                self.item["fields"]["Phone"] != "+375XXXXXXXXX":
            self.person_data["phones"].append((self.item["fields"]["Phone"], 'phone field'))

    def update_addresses(self):
        if "Home Address" in self.item["fields"] and self.item["fields"]["Home Address"]:
            home_addr, home_geo = extract_geoloc_and_address(self.item["fields"]["Home Address"])
            self.person_data["addresses"].append(get_address_dict(
                full_addr=home_addr,
                notes=home_addr,
                position=home_geo,
                address_type=AddressType.HOME_ADDRESS))

        if "Work Address" in self.item["fields"] and self.item["fields"]["Work Address"]:
            work_addr, work_geo = extract_geoloc_and_address(self.item["fields"]["Work Address"])
            self.person_data["addresses"].append(get_address_dict(
                full_addr=work_addr,
                notes=work_addr,
                position=work_geo,
                address_type=AddressType.WORK_ADDRESS))

        if "Location" in self.item["fields"] and self.item["fields"]["Location"]:
            loc_addr, loc_geo = extract_geoloc_and_address(self.item["fields"]["Location"])
            self.person_data["addresses"].append(get_address_dict(
                full_addr=loc_addr,
                notes=loc_addr,
                position=loc_geo,
                address_type=AddressType.LOCATION))
