import pendulum
from typing import Dict
from sqlalchemy import select
from .models import Person
from .utils import get_db


async def get_person_original_dates_by_id(source_type) -> Dict:
    """

    :return:
    """
    q = select(
            [Person.external_id, Person.original_date_time, Person.id]).\
        where(
            Person.source_type == source_type)

    db = get_db()
    res_proxy = db.connect().execute(q)
    res_out = {}
    if res_proxy:
        for item in res_proxy:
            res_out[item["external_id"]] = {
                "original_date_time": pendulum.instance(item["original_date_time"]),
                'id': item["id"],
            }
    return res_out
