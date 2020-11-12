from enum import Enum


class WorkMode(Enum):
    BLACK_BOOK = 'black_book'
    NARUSHITEL = 'narushitel'
    BANDA_LUKI = 'banda_luki'


class SourceType(Enum):
    BLACK_BOOK = 10
    NARUSHITEL = 20
    BANDA_LUKI = 30


class AddressType(Enum):
    HOME_ADDRESS = 10
    WORK_ADDRESS = 20
    LOCATION = 30


class SocialNetworkType(Enum):
    FACEBOOK = 10
    VKONTAKTE = 20
    OK_RU = 30
    INSTAGRAM = 40
    TELEGRAM = 50
    OTHER = 55


class PersonalRelationType(Enum):
    BROTHER = 10
    SISTER = 15
    MOTHER = 20
    FATHER = 25
    SON = 30
    DAUGHTER = 35
    COUSIN = 40
    NEPHEW = 50
    NIECE = 55
    UNCLE = 60
    AUNT = 70
    PARTNER = 100
    COHABITANT_PARTNER = 105
    LOVER = 110
    HUSBAND = 120
    WIFE = 125
    FRIEND = 130
    CO_WORKER = 140
    BOSS = 150
    SUBORDINATE = 160


class PersonType(Enum):
    OTHER = 5           # прочие - БЛ
    PUNISHER = 10       # 'Каратель', 'силовик - БЛ'
    FORGER = 20         # 'Фальсификатор'
    REGIME_ALLY = 30    # 'Пособник Режима'
    JUDGE = 40          # судья - БЛ
    PROPAGANDIST = 50   # пропагандист - БЛ
    OFFICIAL = 60       # чиновник - БЛ


class Gender(Enum):
    MALE = 10
    FEMALE = 20


person_type_narushitel_to_enum = {
    'каратель': PersonType.PUNISHER,
    'фальсификатор': PersonType.FORGER,
    'пособник режима': PersonType.REGIME_ALLY
}


def get_person_type_for_ru_name(nar_name: str):
    if nar_name.lower() in person_type_narushitel_to_enum:
        return person_type_narushitel_to_enum[nar_name.lower()]
    return None
