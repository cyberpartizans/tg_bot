import os
import settings_local


def check_not_empty(dict_setting, setting_name):
    for k, v in dict_setting.items():
        if not v:
            raise ValueError(f"Parameter {k} not set into {setting_name} - can't work!")


TG_CONFIG_TEXT_FILE = "config.txt"
# if set to true, settings for Telegram client must be set in the text file which
# name is stored into TG_CONFIG_TEXT_FILE ("config.txt" by default)
USE_TG_CONFIG_TEXT_FILE = True
PATH_CHROME_DRIVER = os.path.join('external_bin', 'chromedriver')

URL_NARUSHITEL_MAIN = "https://narushitel.org"
URL_NARUSHITEL_KARATELI_WEB = 'https://narushitel.org/karateli'
URL_NARUSHITEL_KARATELI_XHR = 'https://narushitel.org/punishers/'

URL_BANDA_LUKI_WEB_MAIN = 'https://bandaluki.info'
URL_BANDA_LUKI_WEB_MAIN_LIST_PAGES_TPL = 'https://bandaluki.info/page/%d/'
URL_BANDA_LUKI_CATEGORY_LIST_TPL = 'https://bandaluki.info/%s/'
URL_BANDA_LUKI_CATEGORY_LIST_PAGES_TPL = 'https://bandaluki.info/%s/page/%d/'

# <h2 class="entry-title fusion-post-title"><a href="/bandits/aleksa-aleksandr-i/">Алёкса Александр И.</a></h2>
URL_BANDA_LUKI_WEB_PERSON_PAGE_TPL = 'https://bandaluki.info/bandits/%s/'


# MEDIA_PATH_TOP = os.path.join('data', 'files')
MEDIA_PATH_TOP = '/usr/local/var/tg_bot'
PATH_FILES_NARUSHITEL = os.path.join(MEDIA_PATH_TOP, 'narushitel')
PATH_FILES_BLACK_BOOK = os.path.join(MEDIA_PATH_TOP, 'black_book')
PATH_FILES_BLACK_BOOK_TMP = os.path.join(PATH_FILES_BLACK_BOOK, 'tmp')

BETTER_LEXER_IN_PLACE = False  # TODO – заменить на "True", когда будет лучший лексер

DB_PARAMS = {
    "prefix": "",
    "db_name": "",
    "user": "",
    "pass": "",
    "host": "",
    "port": "",
}

TG_CLIENT_SETTINGS = {
    "client_name": "",
    "api_id": 0,
    "api_hash": "",
    "phone": "",
}

if hasattr(settings_local, "DB_PARAMS"):
    DB_PARAMS = settings_local.DB_PARAMS

if hasattr(settings_local, "TG_CLIENT_SETTINGS"):
    TG_CLIENT_SETTINGS = settings_local.TG_CLIENT_SETTINGS


check_not_empty(DB_PARAMS, 'DB_PARAMS')


# if you don't use config.txt, you must set TG_CLIENT_SETTINGS in settings_local.py
if not USE_TG_CONFIG_TEXT_FILE:
    check_not_empty(TG_CLIENT_SETTINGS, 'TG_CLIENT_SETTINGS')
