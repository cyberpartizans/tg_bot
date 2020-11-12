import re
from typing import Optional, List, Dict
from constants import SocialNetworkType
from utils.text.easy_dict import get_social_network_dict
from utils.text.text import clean_str


def find_vks_in_text(text) -> Optional[List]:
    res_out = []
    it = re.finditer(r'(vk.com/(.+?))(\W|\Z)', text)
    for i in it:
        res_out.append(get_social_network_dict(
            type=SocialNetworkType.VKONTAKTE,
            url='https://' + clean_str(i.groups()[0]),
            net_user_id=clean_str(i.groups()[1])))
    return res_out


def find_oks_in_text(text) -> Optional[List]:
    res_out = []
    it = re.finditer(r'(ok.ru/profile/([0-9A-Za-z_-]+))|(ok.ru/([0-9A-Za-z_-]+))(\W|\Z)', text)
    for i in it:
        if i.groups()[0] and i.groups()[1]:
            res_out.append(get_social_network_dict(
                type=SocialNetworkType.OK_RU,
                url='https://' + clean_str(i.groups()[0]),
                net_user_id=clean_str(i.groups()[1])))
        elif i.groups()[2] and i.groups()[3]:
            res_out.append(get_social_network_dict(
                type=SocialNetworkType.OK_RU,
                url='https://' + clean_str(i.groups()[2]),
                net_user_id=clean_str(i.groups()[3])))
    return res_out


def find_fbs_in_text(text) -> Optional[List]:
    res_out = []
    it = re.finditer(r'(facebook.com/(.+?))(\W|\Z)', text)
    for i in it:
        res_out.append(get_social_network_dict(
            type=SocialNetworkType.FACEBOOK,
            url='https://' + clean_str(i.groups()[0]),
            net_user_id=clean_str(i.groups()[1])))
    return res_out


def find_instagrams_in_text(text) -> Optional[List]:
    res_out = []
    it = re.finditer(r'(instagram.com/(.+?))(\W|\Z)', text)
    for i in it:
        res_out.append(get_social_network_dict(
            type=SocialNetworkType.INSTAGRAM,
            url='https://' + clean_str(i.groups()[0]),
            net_user_id=clean_str(i.groups()[1])))
    return res_out


def find_telegrams_in_text(text) -> Optional[List]:
    res = [clean_str(i) for i in re.findall(r"\@\w+", text) if not re.search('_blacklist_bot', i, re.I)]
    res_out = []
    for i in res:
        res_out.append(get_social_network_dict(
            type=SocialNetworkType.TELEGRAM,
            url=i,
            net_user_id=i))
    return res_out


def get_social_link_in_text_for_data_type(data_type: str, item_clean: str, label: str) -> List[Dict]:
    """

    :param data_type:
    :param item_clean:
    :param label:
    :return:
    """
    finders_for_datatypes = {
        "social_fbs": find_fbs_in_text,
        "social_vks": find_vks_in_text,
        "social_oks": find_oks_in_text,
        "social_instagrams": find_instagrams_in_text,
        "social_telegrams": find_telegrams_in_text
    }
    if data_type not in finders_for_datatypes:
        return []
    finder = finders_for_datatypes[data_type]
    res = finder(item_clean)
    for i in res:
        i["notes"] = label
    return res
