import re
from typing import Dict


def is_person_by_full_name(full_name: str) -> bool:
    """
    используется только парсером black_book
    :param full_name:
    :return:
    """
    words = re.findall(r"\w+", full_name)
    if not words:
        return False
    # 3 слова (имя, отчество, фамилия), но мы оставляем 2 больше на всяки случай
    if len(words) > 5:
        return False
    return True


def split_full_name(full_name: str) -> Dict:
    # TODO - надо найти способ, чтобы правильно разделить босточнославянские (русские, беларуские, украинские) имена.
    #  Источники НЕ соблюдают порядок ФИО (Фамилия, Имя, Отчество), в некоторых случаях это фамилия + отчество + имя
    #  или другое.
    #  Мы не можем определить это без хорошего лексера имени. НАДО ИМЕТЬ ЛУЧШИЙ ЛЕКСЕР!!!
    res = {
        "first_name": "",
        "middle_name": "",
        "last_name": "",
    }
    return res
