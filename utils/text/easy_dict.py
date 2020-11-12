from typing import Dict


def _set_in_dict_if_field_defined(vals_to_set: Dict, res: Dict):
    """

    :param vals_to_set:
    :param res:
    :return:
    """
    for key, value in vals_to_set.items():
        if key not in res:
            raise KeyError(f"Key '{key}' not allowed")
        res[key] = value


def get_address_dict(**kwargs):
    """

    :param kwargs:
    :return:
    """
    res = {
        "source_id": None,    # TODO - зачем нам эта таблица? Пусть решим это.
        "full_addr": "",
        "address_type": None,
        "position": None,
        # -- TODO - нам нужен механизм (лексер?) для парсинга адресов
        "country": "",
        "city": "",
        "region": "",
        "district": "",
        "building": "",
        "block": "",
        "appartment": "",
        # /-- TODO - нам нужен механизм (лексер?) для парсинга адресов
        "from_date": None,  # TODO - сейчас невозможно получить эти данные из наших источников
        "to_date": None,    # TODO - сейчас невозможно получить эти данные из наших источников
        "notes": "",
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_document_dict(**kwargs):
    """

    :param kwargs:
    :return:
    """
    res = {
        "source_id": None,
        # TODO - нужен механизм (лексер?) для парсинга данных документов
        "type": None,
        "title": "",
        "serial_number": None,
        "valid_from": None,  # TODO - сейчас невозможно получить эти данные из наших источников
        "valid_to": None,    # TODO - сейчас невозможно получить эти данные из наших источников
        # /TODO - нужен механизм (лексер?) для парсинга данных документов
        "notes": ""
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_social_network_dict(**kwargs):
    res = {
        "source_id": None,
        "type": None,
        "url": "",
        # TODO - чтобы прочитать название пользователя в сети, надо авторизобаться в системе,
        #  поэтому надо это делать в другом скрипте
        "net_name": "",
        "net_user_id": "",
        "notes": "",
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_phone_dict(**kwargs):
    res = {
        "source_id": None,
        "number": "",
        "notes": "",
        "normalized": "",   # TODO - создать конвертер телефонных номеров
        "carrier": "",      # TODO - сейчас невозможно получить эти данные из наших источников
        "from_date": None,    # TODO - сейчас невозможно получить эти данные из наших источников
        "to_date": None,      # TODO - сейчас невозможно получить эти данные из наших источников
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_job_dict(**kwargs):
    res = {
        "employer_id": None,      # TODO - нам нужен список организаций/институций, которые мы свяжем с лицами
        "source_id": None,        # TODO - зачем нам эта таблица? Пусть решим это.
        "position": "",
        "notes": "",
        "from_date": None,
        "to_date": None,
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_email_dict(**kwargs):
    res = {
        "source_id": None,
        "email": "",
        "notes": "",
        "from_date": None,
        "to_date": None,
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_car_dict(**kwargs):
    res = {
        "id": None,
        "address_id": None,
        "source_id": None,
        "owner_id": None,
        "person_id": None,
        "type": "",
        "brand": "",
        "model": "",
        "license_plate": "",
        "color": "",
        "from_date": None,
        "to_date": None,
        "production_year": None,
        "registration_year": None,
        "vin": "",
        "notes": "",
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res


def get_person_dict(**kwargs):
    res = {
        "id": None,
        "source_id": None,
        "source_type": None,
        "external_id": None,
        "original_date_time": None,
        "parsing_date_time": None,
        "full_name": "",
        "last_name": "",
        "first_name": "",
        "middle_name": "",
        "gender": None,
        "birth_date": None,
        "origin_place": "",
        "identity_number": "",
        "passport_number": "",
        "passport_issue_date": None,
        "passport_issue_place": "",
        "rank": "",
        "last_known_location": None,
        "notes": "",
        "media_items": None,
        "incidents": None,
        "types": None,
        "personal_relations": None,
        "addresses": None,
        "properties": None,
        "documents": None,
        "owned_vehicles": None,
        "used_vehicles": None,
        "jobs": None,
        "social_networks": None,
        "phones": None,
        "emails": None,
    }
    _set_in_dict_if_field_defined(kwargs, res)
    return res

