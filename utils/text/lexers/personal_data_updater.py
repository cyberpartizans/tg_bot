from typing import Dict, List
from utils.text.text import clean_found_item
from utils.text.easy_dict import get_address_dict, get_document_dict, get_job_dict, get_phone_dict, \
    get_email_dict, get_car_dict, get_person_dict
from .social import get_social_link_in_text_for_data_type
from utils.text.lexers.data.phrases import base_lexer_phrases
from utils.text.lexers.data.funcs import base_lexer_criteria_funcs
import settings


def update_person_data_using_lexers(text: str, person_data, phrases=None, criteria_funcs=None) -> bool:
    """

    :param text:
    :param person_data:
    :param phrases:
    :param criteria_funcs:
    :return:
    """
    cur_frag_type = ''
    cur_frag_label = ''
    cur_frag_begin = -1
    len_text = len(text)
    i = 0
    phrases = phrases if phrases else base_lexer_phrases
    criteria_funcs = criteria_funcs if criteria_funcs else base_lexer_criteria_funcs
    while i < len_text:
        jumped = False
        for p_d in phrases:
            p_text: str = str(p_d["text"])
            p_type: str = str(p_d["type"])
            # print("\n\n P_TEXT ", p_text, "P_TYPE ", p_type)
            if text[i: i + len(p_text)].lower() == p_text.lower():
                if cur_frag_type and cur_frag_begin >= 0:
                    add_parsed_item_to_person_data(
                        cur_frag_type,
                        text[cur_frag_begin: i],
                        cur_frag_label,
                        person_data,
                        criteria_funcs)
                cur_frag_type = p_type
                if p_d["keep_label"]:
                    cur_frag_label = p_text
                else:
                    cur_frag_label = ''
                cur_frag_begin = i + len(p_text)
                i += len(p_text)
                jumped = True
                break  # we don't want to analyze the next phrase again when we found one
        if not jumped:
            i += 1

    if cur_frag_type and cur_frag_begin >= 0:
        add_parsed_item_to_person_data(
            cur_frag_type,
            text[cur_frag_begin:],
            cur_frag_label,
            person_data,
            criteria_funcs)
    return False


def add_parsed_item_to_person_data(
        data_type: str, item: str, label: str, person_data: Dict, criteria_funcs: Dict, *args):
    """

    :param data_type:
    :param item:
    :param label:
    :param person_data:
    :param criteria_funcs:
    :param args:
    :return:
    """

    if data_type in criteria_funcs:
        for func in criteria_funcs[data_type]:
            if not func(item):   # can't add an item because it doesn't pass the criteria
                return

    item_clean = clean_found_item(item)
    item_clean_short = item_clean[0:255] if item_clean else ""
    if label and item_clean:
        notes_full = label + " :: " + item_clean
    elif label:
        notes_full = label
    elif item_clean:
        notes_full = item_clean
    else:
        notes_full = ""

    if data_type == 'addresses':
        i: Dict
        if item_clean not in [i['full_addr'] for i in person_data[data_type]]:  # не хотим дубликатов
            person_data[data_type].append(get_address_dict(full_addr=item_clean_short, notes=notes_full))
    elif data_type == 'documents':
        i: Dict
        person_data[data_type].append(get_document_dict(title=item_clean_short, notes=notes_full))
    elif data_type in ["social_fbs", "social_vks", "social_oks", "social_instagrams", "social_telegrams"]:
        i: Dict
        res: List[Dict] = get_social_link_in_text_for_data_type(data_type, item_clean, label)
        if res:
            person_data[data_type].extend(res)
    elif data_type == 'roles':
        person_data[data_type].append(get_job_dict(position=item_clean_short, notes=notes_full))
    elif data_type == 'phones':
        person_data[data_type].append(get_phone_dict(number=item_clean_short, notes=notes_full))
    elif data_type == 'emails':
        person_data[data_type].append(get_email_dict(email=item_clean_short, notes=notes_full))
    elif data_type == 'cars':
        # TODO - еще не пора добавлять машины, качество данных будет плохое. надо сделать лучший лексер.
        if settings.BETTER_LEXER_IN_PLACE:
            person_data[data_type].append(get_car_dict(model=item_clean_short, notes=notes_full))
    elif data_type == 'family_members':
        # TODO - еще не пора добавлять машины, качество данных будет плохое. надо сделать лучший лексер.
        if settings.BETTER_LEXER_IN_PLACE:
            person_data[data_type].append(get_person_dict(full_name=item_clean_short, notes=notes_full))
