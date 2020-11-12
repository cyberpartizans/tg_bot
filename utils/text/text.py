import re
import pendulum
from typing import Optional, List


def clean_str(text: str) -> str:
    """

    :param text:
    :return:
    """
    return text.strip()


def clean_found_item(text: str) -> str:
    """

    :param text:
    :return:
    """
    text = text.strip("\n\t\r\f\v :")
    text = re.sub("\n|\r|\t", " ", text)
    return text


def date_from_text_to_obj(date_text: str, date_format: str = 'YYYY-MM-DD'):
    """

    :param date_text:
    :param date_format:
    :return:
    """
    if not date_text or not date_format:
        return None
    try:
        dt_obj = pendulum.from_format(date_text, date_format)
        return dt_obj
    except ValueError:
        return None


def iso_date_to_obj(date_text: str):
    """

    :param date_text:
    :return:
    """
    if not date_text:
        return None
    try:
        dt_obj = pendulum.parse(date_text)
        return dt_obj
    except ValueError:
        return None
    except pendulum.parsing.exceptions.ParserError:
        return None
    except Exception:
        return None


def narushitel_url_into_path(url: str, fid: Optional[str] = None) -> str:
    """

    :param url:
    :param fid:
    :return:
    """
    # URL-адреса всегда имеют косую черту (никогда не обратную косую черту),
    # а os.path.split разбивается на две части, когда нам нужно больше деталей
    url_list = url.strip('/').split("/")
    if fid:
        res = fid + '==' + '--'.join(url_list[1:])
    else:
        res = '--'.join(url_list[1:])
    return res


def narushitel_path_into_url(path: str) -> str:
    """

    :param path:
    :return:
    """

    # удаляет начальный идентификатор
    x = re.search('.+==(.+)', path)
    if x:
        path = x.groups()[0]

    path_list: List = ['img'] + path.split("--")
    return "/" + "/".join(path_list)
