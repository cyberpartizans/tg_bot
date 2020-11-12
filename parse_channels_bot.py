import asyncio
import argparse
from utils.telegram import get_telegram_client, authorize
from utils.db_adder import database_item_adder
from readers.black_book.reader import Reader as ReaderBBB
from parsers.black_book.list_parser import ListParser as ListParserBBB
from readers.narushitel.reader import Reader as ReaderNar
from parsers.narushitel.list_parser import ListParser as ListParserNar
from readers.banda_luki.reader import Reader as ReaderBL
from constants import WorkMode, SourceType
from db.db_ops import get_person_original_dates_by_id
from typing import Dict


modes = []
loop = asyncio.get_event_loop()

ap = argparse.ArgumentParser(
    add_help=True,
    description="Parser of Karatel data from external sources")
ap.add_argument(
    "-b", "--bbb",
    required=False,
    action="store_true",
    help="Black Book of Belarus (Черная Книга Беларуси)")

ap.add_argument(
    "-n", "--narushitel",
    required=False,
    action="store_true",
    help="Narushitel.org")

ap.add_argument(
    "-l", "--bandaluki",
    required=False,
    action="store_true",
    help="bandaluki.info")


args = vars(ap.parse_args())
if args['bbb']:
    modes.append(WorkMode.BLACK_BOOK)
if args['narushitel']:
    modes.append(WorkMode.NARUSHITEL)

if args['bandaluki']:
    modes.append(WorkMode.BANDA_LUKI)

if not modes:
    modes.append(WorkMode.NARUSHITEL)


async def process_black_book():
    client = await get_telegram_client()
    await authorize(client)
    reader_bbb = ReaderBBB(client)
    list_parser_bbb = ListParserBBB(client)
    items = await reader_bbb.find_items()
    orig_dates: Dict = await get_person_original_dates_by_id(SourceType.BLACK_BOOK)
    print("\n orig dates ", orig_dates)
    async for item in list_parser_bbb.parse_all_items_gen(items):
        await database_item_adder(item, SourceType.BLACK_BOOK, orig_dates)


async def process_narushitel():
    reader_nar = ReaderNar()
    list_parser_nar = ListParserNar()

    items = await reader_nar.find_items()
    orig_dates: Dict = await get_person_original_dates_by_id(SourceType.NARUSHITEL)
    async for item in list_parser_nar.parse_all_items_gen(items):
        await database_item_adder(item, SourceType.NARUSHITEL, orig_dates)


async def process_banda_luki():
    reader_bl = ReaderBL()
    items = await reader_bl.find_items()


if WorkMode.BLACK_BOOK in modes:
    loop.run_until_complete(process_black_book())
if WorkMode.NARUSHITEL in modes:
    loop.run_until_complete(process_narushitel())
if WorkMode.BANDA_LUKI in modes:
    loop.run_until_complete(process_banda_luki())
