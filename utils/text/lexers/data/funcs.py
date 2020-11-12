from typing import Dict
from utils.text.lexers.phone import check_phone_found


base_lexer_criteria_funcs: Dict = {
    'phones': [
        check_phone_found,
    ],
}
