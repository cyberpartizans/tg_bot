import pendulum
from typing import List, Dict
from db.utils import get_db, get_db_session
from db.models import Person, Media, Job, Address, Document, PersonType, SocialNetwork, Phone, Vehicle, Email
from db.db_ops import get_person_original_dates_by_id
import settings


async def database_item_adder(item: Dict, source_type, orig_dates) -> None:
    """

    :param parsed_items:
    :param source_type:
    :return:
    """
    db = get_db()
    ses = get_db_session(db)

    parsing_dt = pendulum.now()

    # важно для Черной Книги Беларуси, где id - численные
    ext_id = str(item["external_id"])

    # элемент существует в базе и актуален - не надо обновлять или добавлять его - пропускаю
    if ext_id in orig_dates and item["item_date"] <= orig_dates[ext_id]['original_date_time']:
        print("\nElement %s up-to-date - skipping." % ext_id)
        return
    elif ext_id in orig_dates:  # элемент надо обновить
        print("\nElement %s is outdated - updating." % ext_id)
        pid = orig_dates[ext_id]["id"]
        await update_person(item, pid, parsing_dt, ses)
    else:  # элемент надо добавить в базу
        print("\nElement %s not found in our database - adding" % ext_id)
        await add_person(item, parsing_dt, source_type, ses)


async def add_person(item: Dict, parsing_dt, source_type, ses) -> None:
    """

    :param item:
    :param parsing_dt:
    :param source_type:
    :param ses:
    :return:
    """
    person = Person(
        external_id=item["external_id"],
        original_date_time=item["item_date"],
        parsing_date_time=parsing_dt,
        source_id=item["source_id"],
        source_type=source_type,
        full_name=item["full_name"],
        first_name=item["first_name"],
        middle_name=item["middle_name"],
        last_name=item["last_name"],
        gender=item["gender"],
        origin_place=item["origin_place"],
        identity_number=item["identity_number"],
        passport_number=item["passport_number"],
        passport_issue_date=item["passport_issue_date"],
        passport_issue_place=item["passport_issue_place"],
        rank=item["title"],
        birth_date=item["date_of_birth"],
        notes=item["notes"]
    )
    ses.add(person)
    save_person_related_features(person, item, ses, parsing_dt)


async def update_person(item, pid, parsing_dt, ses):
    """

    :param item:
    :param pid:
    :param parsing_dt:
    :param ses:
    :return:
    """
    person = ses.query(Person).get(pid)
    person.original_date_time = item["item_date"]
    person.parsing_date_time = parsing_dt
    person.full_name = item["full_name"],
    person.first_name = item["first_name"]
    person.middle_name = item["middle_name"]
    person.last_name = item["last_name"]
    person.gender = item["gender"]
    person.origin_place = item["origin_place"]
    person.identity_number = item["identity_number"]
    person.passport_number = item["passport_number"]
    person.passport_issue_date = item["passport_issue_date"]
    person.passport_issue_place = item["passport_issue_place"]
    person.rank = item["title"]
    person.birth_date = item["date_of_birth"]
    person.notes = item["notes"]

    # уже используется

    for i in person.addresses:
        ses.delete(i)

    for i in person.documents:
        ses.delete(i)

    for i in person.emails:
        ses.delete(i)

    for i in person.jobs:
        ses.delete(i)

    for i in person.media_items:
        ses.delete(i)

    for i in person.phones:
        ses.delete(i)

    for i in person.social_networks:
        ses.delete(i)

    for i in person.types:
        ses.delete(i)
    ses.commit()  # нужно после удаления, в другом случае выдает ошибку

    # TODO - еще не используется
    if settings.BETTER_LEXER_IN_PLACE:
        for i in person.incidents:
            ses.delete(i)

        for i in person.owned_vehicles:
            ses.delete(i)

        for i in person.used_vehicles:
            ses.delete(i)

        for i in person.personal_relations:
            ses.delete(i)

        for i in person.properties:
            ses.delete(i)

    ses.add(person)
    save_person_related_features(person, item, ses, parsing_dt)


def save_person_related_features(person, item, ses, parsing_dt):
    """

    :param person:
    :param item:
    :param ses:
    :param parsing_dt:
    :return:
    """
    for person_type in item["types"]:
        p_t = PersonType(type=person_type)
        person.types.append(p_t)

    for p_info in item["photos"]:
        media = Media(
            external_id=p_info["external_id"],
            size=p_info["size"],
            type=p_info["type"],
            original_url=p_info["external_url"],
            file_name=p_info["file_name"],
            url=p_info["original_file_name"]
        )
        person.media_items.append(media)

    for role_info in item["roles"]:
        job = Job(
            employer_id=role_info["employer_id"],
            source_id=role_info["source_id"],
            position=role_info["position"],
            notes=role_info["notes"],
            from_date=role_info["from_date"],
            to_date=role_info["to_date"],
        )
        person.jobs.append(job)

    for addr_info in item["addresses"]:
        if addr_info["position"] and len(addr_info["position"]) ==2:
            pos = 'SRID=4326;POINT (%s %s )' % (addr_info["position"][0], addr_info["position"][1])
        else:
            pos = None
        address = Address(
            source_id=addr_info["source_id"],
            full_addr=addr_info["full_addr"],
            address_type=addr_info["address_type"],
            position=pos,
            country=addr_info["country"],
            city=addr_info["city"],
            region=addr_info["region"],
            district=addr_info["district"],
            building=addr_info["building"],
            block=addr_info["block"],
            appartment=addr_info["appartment"],
            from_date=addr_info["from_date"],
            to_date=addr_info["to_date"],
            notes=addr_info["notes"]
        )
        person.addresses.append(address)

    for doc_info in item["documents"]:
        doc = Document(
            source_id=doc_info["source_id"],
            type=doc_info["type"],
            title=doc_info["title"],
            serial_number=doc_info["serial_number"],
            valid_from=doc_info["valid_from"],
            valid_to=doc_info["valid_to"],
            notes=doc_info["notes"]
        )
        person.documents.append(doc)

    for fb_link in item["social_fbs"]:
        soc = SocialNetwork(
            source_id=fb_link["source_id"],
            type=fb_link["type"],
            url=fb_link["url"],
            net_name=fb_link["net_name"],
            net_user_id=fb_link["net_user_id"]
        )
        person.social_networks.append(soc)

    for vk_link in item["social_vks"]:
        soc = SocialNetwork(
            source_id=vk_link["source_id"],
            type=vk_link["type"],
            url=vk_link["url"],
            net_name=vk_link["net_name"],
            net_user_id=vk_link["net_user_id"]
        )
        person.social_networks.append(soc)

    for ok_link in item["social_oks"]:
        soc = SocialNetwork(
            source_id=ok_link["source_id"],
            type=ok_link["type"],
            url=ok_link["url"],
            net_name=ok_link["net_name"],
            net_user_id=ok_link["net_user_id"]
        )
        person.social_networks.append(soc)

    for insta_link in item["social_instagrams"]:
        soc = SocialNetwork(
            source_id=insta_link["source_id"],
            type=insta_link["type"],
            url=insta_link["url"],
            net_name=insta_link["net_name"],
            net_user_id=insta_link["net_user_id"]
        )
        person.social_networks.append(soc)

    for tele_link in item["social_telegrams"]:
        soc = SocialNetwork(
            source_id=tele_link["source_id"],
            type=tele_link["type"],
            url=tele_link["url"],
            net_name=tele_link["net_name"],
            net_user_id=tele_link["net_user_id"]
        )
        person.social_networks.append(soc)

    for phone_info in item["phones"]:
        phone = Phone(
            source_id=phone_info["source_id"],
            notes=phone_info["notes"],
            normalized=phone_info["normalized"],
            number=phone_info["number"],
            carrier=phone_info["carrier"],
            from_date=phone_info["from_date"],
            to_date=phone_info["to_date"]
        )
        person.phones.append(phone)

    for email_info in item["emails"]:
        email = Email(
            source_id=email_info["source_id"],
            email=email_info["email"],
            notes=email_info["notes"],
            from_date=email_info["from_date"],
            to_date=email_info["to_date"]
        )
        person.emails.append(email)

    # TODO - сейчас нет змысла добавлять данные машин. Во-первых,
    #  нам надо найти хороший лексер для обработки текста.
    if settings.BETTER_LEXER_IN_PLACE:
        for car_info in item["cars"]:
            car = Vehicle(
                address_id=car_info["address_id"],
                source_id=car_info["source_id"],
                owner_id=car_info["owner_id"],
                person_id=car_info["person_id"],
                type=car_info["type"],
                brand=car_info["brand"],
                model=car_info["model"],
                license_plate=car_info["license_plate"],
                color=car_info["color"],
                from_date=car_info["from_date"],
                to_date=car_info["to_date"],
                production_year=car_info["production_year"],
                registration_year=car_info["registration_year"],
                vin=car_info["vin"],
                notes=car_info["notes"]
            )
            person.used_vehicles.append(car)

        for mem_info in item["family_members"]:
            mem = Person(
                source_id=mem_info["source_id"],
                source_type=mem_info["source_type"],
                external_id=mem_info["external_id"],
                original_date_time=mem_info["original_date_time"],
                parsing_date_time=mem_info["parsing_date_time"],
                full_name=mem_info["full_name"],
                last_name=mem_info["last_name"],
                first_name=mem_info["first_name"],
                middle_name=mem_info["middle_name"],
                gender=mem_info["gender"],
                birth_date=mem_info["birth_date"],
                origin_place=mem_info["origin_place"],
                identity_number=mem_info["identity_number"],
                passport_number=mem_info["passport_number"],
                passport_issue_date=mem_info["passport_issue_date"],
                passport_issue_place=mem_info["passport_issue_place"],
                rank=mem_info["rank"],
                last_known_location=mem_info["last_known_location"],
                notes=mem_info["notes"],
                media_items=mem_info["media_items"],
                incidents=mem_info["incidents"],
                types=mem_info["types"],
                personal_relations=mem_info["personal_relations"],
                addresses=mem_info["addresses"],
                properties=mem_info["properties"],
                documents=mem_info["documents"],
                owned_vehicles=mem_info["owned_vehicles"],
                used_vehicles=mem_info["used_vehicles"],
                jobs=mem_info["jobs"],
                social_networks=mem_info["social_networks"],
                phones=mem_info["phones"],
                emails=mem_info["emails"],
            )
            ses.add(mem)

    ses.commit()
