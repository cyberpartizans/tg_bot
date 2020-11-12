from typing import List, Dict, Union


phrases: List[Dict[str, Union[str, bool]]] = [
    {"text": "страница жены в вк", "type": "social_vks", "keep_label": True},
    {"text": "vk его жены", "type": "social_vks", "keep_label": True},
    {"text": "vk жены", "type": "social_vks", "keep_label": True},
    {"text": "страница жены в одноклассниках", "type": "social_oks", "keep_label": True},
    {"text": "женат", "type": "family_members", "keep_label": True},
    {"text": "жена", "type": "family_members", "keep_label": True},
    {"text": "есть дочь", "type": "family_members", "keep_label": True},
    {"text": "дочь", "type": "family_members", "keep_label": True},
    {"text": "адрес прописки", "type": "addresses", "keep_label": True},
    {"text": "адрес проживания", "type": "addresses", "keep_label": True},
    {"text": "почтовый адрес", "type": "addresses", "keep_label": True},
    {"text": "адреса", "type": "addresses", "keep_label": False},
    {"text": "адресу", "type": "addresses", "keep_label": False},
    {"text": "предположительный адрес", "type": "addresses", "keep_label": True},
    {"text": "адрес", "type": "addresses", "keep_label": False},
    {"text": "место жительства", "type": "addresses", "keep_label": True},
    {"text": "возможный рабочий телефон", "type": "phones", "keep_label": True},
    {"text": "рабочие телефоны", "type": "phones", "keep_label": True},
    {"text": "рабочий телефон", "type": "phones", "keep_label": True},
    {"text": "домашний телефон", "type": "phones", "keep_label": True},
    {"text": "мобильный телефон", "type": "phones", "keep_label": True},
    {"text": "мобильный", "type": "phones", "keep_label": True},
    {"text": "предполагаемый телефон", "type": "phones", "keep_label": True},
    {"text": "телефон для брони", "type": "phones", "keep_label": True},
    {"text": "предполагаемый номер", "type": "phones", "keep_label": True},
    {"text": "телефоны", "type": "phones", "keep_label": True},
    {"text": "телефон", "type": "phones", "keep_label": True},
    {"text": "тел.", "type": "phones", "keep_label": True},
    {"text": "cредполагаемый номер", "type": "phones", "keep_label": True},
    {"text": "паспортные данные жены", "type": "documents", "keep_label": True},
    {"text": "паспортные данные", "type": "documents", "keep_label": True},
    {"text": "серия и номер паспорта", "type": "documents", "keep_label": True},
    {"text": "номер паспорта", "type": "documents", "keep_label": True},
    {"text": "паспорт серия и номер", "type": "documents", "keep_label": True},
    {"text": "паспорт", "type": "documents", "keep_label": True},
    {"text": "личный номер", "type": "documents", "keep_label": True},
    {"text": "личная машина", "type": "cars", "keep_label": True},
    {"text": "номер машины", "type": "cars", "keep_label": True},
    {"text": "личный автомобиль", "type": "cars", "keep_label": False},
    {"text": "авто", "type": "cars", "keep_label": True},
    {"text": "фейсбук", "type": "social_fbs", "keep_label": False},
    {"text": "почта", "type": "emails", "keep_label": True},
]
