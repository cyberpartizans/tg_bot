import re
import pendulum
from typing import Optional, Match


_months_genitive_word = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июна",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


# также используется для парсинга - удаления дат
def _find_date_numeric_re_match(block: str) -> Optional[Match[str]]:
    """

    :param block:
    :return:
    """
    test_dob = re.search(r"([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})", block, re.I)
    return test_dob


# также используется для парсинга - удаления дат
def _find_date_nominal_re_match(block: str) -> Optional[Match[str]]:
    """

    :param block:
    :return:
    """
    test_dob = re.search(r"([0-9]{1,2}) (" + "|".join(_months_genitive_word) +
                         ") ([0-9]{4})( года)?", block.lower(), re.I)
    return test_dob


def find_date_in_text(block: str):
    """
    ищет дату рождения, возвращает объект datetime.date
    :param block:
    :return: (pendulum.datetime, original_date_text: str)
    """
    test_dob = _find_date_numeric_re_match(block)
    if test_dob:
        test_day = int(test_dob.groups()[0].lstrip("0"))
        test_month = int(test_dob.groups()[1].lstrip("0"))
        test_year = int(test_dob.groups()[2])
        if 1 <= test_day <= 31 and \
                1 <= test_month <= 12 and \
                1900 <= test_year <= pendulum.today(tz="UTC").year:
            return pendulum.datetime(year=test_year, month=test_month, day=test_day), test_dob.group()

    test_dob = _find_date_nominal_re_match(block)
    if test_dob:
        test_day = int(test_dob.groups()[0].lstrip("0"))
        month_name = test_dob.groups()[1]
        test_month = _months_genitive_word.index(month_name.lower()) + 1
        test_year = int(test_dob.groups()[2])
        if 1 <= test_day <= 31 and \
                1 <= test_month <= 12 and \
                1900 <= test_year <= pendulum.today(tz="UTC").year:
            return pendulum.datetime(year=test_year, month=test_month, day=test_day), test_dob.group()

    return None, None


def possible_adult_person_dob(p_date) -> bool:
    """
    проверяет, может ли дата быть датой рождения взрослого человека?
    :param p_date:
    :return:
    """
    dt_today = pendulum.today(tz="UTC")
    if (dt_today - p_date).years >= 18:
        return True
    return False
