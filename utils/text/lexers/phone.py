import re
from typing import List


def check_phone_found(text: str) -> bool:
    """

    :param text:
    :return:
    """
    if find_phone_numbers(text):
        return True
    return False


def find_phone_numbers(text: str) -> List:
    """

    :param text:
    :return:
    """
    # TODO - найти другие номера, например начиная с 8, служебные номера в виде XX–YYY и т.д.
    #   также надо разобрать описание номера, обычно оно слева (требуется выборка
    #   слова слева или получение позиции и проверка в цикле - не в findall)
    # finds +375XXXYYYZZZ, 375XXXYYYZZZ, +375 (XX) X-YYY-ZZZ etc.
    res = re.finditer(r'(\+?375[0-9\-()\s]+)', text)
    res_out = []
    for item in res:
        res_out.append(item.groups()[0])
    return res_out


def find_phone_numbers_lax(text: str) -> List:
    """
    эта функция проверяет, является ли это телефон, только по наличию цифр, пробелов, скобок и тире
    :param text:
    :return:
    """
    res = re.finditer(r'([()+0-9\s-]+)', text)
    res_out = []
    for item in res:
        res_out.append(item.groups()[0])
