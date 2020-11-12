import re
from typing import Tuple, Optional


def extract_geoloc_and_address(address_text) -> Tuple[str, Optional[Tuple[float, float]]]:
    x = re.search(r'\[([0-9]+\.[0-9]+),\s([0-9]+\.[0-9]+)\](.+)', address_text)
    if x:
        lat = float(x.groups()[0])
        lng = float(x.groups()[1])
        addr = x.groups()[2]
        return addr.strip(), (lat, lng)
    else:
        return address_text.strip(), None
