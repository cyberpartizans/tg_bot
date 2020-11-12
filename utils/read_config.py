import os
from typing import Tuple
import settings


def read_config() -> Tuple[str, int, str, str]:
    if settings.USE_TG_CONFIG_TEXT_FILE:  # use config file (usually config.txt)
        if not settings.TG_CONFIG_TEXT_FILE:
            raise OSError("No config file set.")

        if not os.path.exists(settings.TG_CONFIG_TEXT_FILE):
            raise OSError(f"Config file {settings.TG_CONFIG_TEXT_FILE} does not exist")
        with open(settings.TG_CONFIG_TEXT_FILE) as reader:
            lines = reader.readlines()
            if len(lines) < 4:
                raise OSError(f"Config file {settings.TG_CONFIG_TEXT_FILE} is incomplete.")
            client_name: str = lines[0][:-1]
            api_id: int = int(lines[1][:-1])
            api_hash: str = lines[2][:-1]
            phone_number: str = lines[3][:-1]
        if not client_name or not api_id or not api_hash or not phone_number:
            raise OSError(f"Missing config data in {settings.USE_TG_CONFIG_TEXT_FILE}")

        return client_name, api_id, api_hash, phone_number
    else:  # use settings
        if not settings.TG_CLIENT_SETTINGS or \
                "client_name" not in settings.TG_CLIENT_SETTINGS or \
                not settings.TG_CLIENT_SETTINGS["client_name"] or \
                "api_id" not in settings.TG_CLIENT_SETTINGS or \
                "api_hash" not in settings.TG_CLIENT_SETTINGS or \
                "phone" not in settings.TG_CLIENT_SETTINGS:
            raise OSError("missing parameters in settings.TG_CLIENT_SETTINGS")
        return settings.TG_CLIENT_SETTINGS["client_name"], \
            settings.TG_CLIENT_SETTINGS["api_id"], \
            settings.TG_CLIENT_SETTINGS["api_hash"], \
            settings.TG_CLIENT_SETTINGS["phone"]

