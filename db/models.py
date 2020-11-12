from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Date, DateTime, \
    BigInteger, SmallInteger, Sequence, ForeignKey, Enum
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from constants import SocialNetworkType, PersonalRelationType, PersonType as PersonTypeEnum, \
    SourceType, AddressType, Gender


Base = declarative_base()
meta = Base.metadata


class PersonType(Base):
    __tablename__ = "person_type"
    id = Column(Integer, Sequence("person_type_id_seq"), primary_key=True)
    person_id = Column(BigInteger, ForeignKey("person.id"), nullable=False)
    type = Column(Enum(PersonTypeEnum), index=True)
    type_desc = Column(Text)  # field for unusual cases, when there is no category set in Enum

    def __repr__(self):
        return f"<PersonType(name={self.person_id}, type={self.type}, type_desc={self.type_desc})>"


# ---- relationships between tables (отношения между таблицами)
class PersonIncident(Base):
    __tablename__ = "person_incident"
    person_id = Column(BigInteger, ForeignKey("person.id"), primary_key=True)
    incident_id = Column(BigInteger, ForeignKey("incident.id"), primary_key=True)


# TODO - я думаю, есть ли это отношение нужно? Медия (фотки и т.д.) - обычно связаны с одном человеком.
class PersonMedia(Base):
    __tablename__ = "person_media"
    person_id = Column(BigInteger, ForeignKey("person.id"), primary_key=True)
    media_id = Column(BigInteger, ForeignKey("media.id"), primary_key=True)
    source_id = Column(BigInteger, ForeignKey("source.id"))


# отношение между лицами
class PersonPerson(Base):
    __tablename__ = "person_person"
    from_person_id = Column(BigInteger, ForeignKey("person.id", name="from_person"))
    to_person_id = Column(BigInteger, ForeignKey("person.id", name="to_person"))

    # from_person = relationship("Person", foreign_keys="Person.id")
    # to_person = relationship("Person", foreign_keys="Person.id")

    source_id = Column(BigInteger, ForeignKey("source.id"))
    type = Column(Enum(PersonalRelationType), primary_key=True)
    # описание отношения, например "любовница", "брат", "мать" и т.д.; должно быть согнасным с полем "type"
    description = Column(Text)
    from_date = Column(Date)
    # -- Если по-прежнему используется, то to_date=null
    to_date = Column(Date)


# новая таблица - медия для документов (например сканы)
class DocumentMedia(Base):
    __tablename__ = "document_media"
    document_id = Column(BigInteger, ForeignKey("document.id"), primary_key=True)
    media_id = Column(BigInteger, ForeignKey("media.id"), primary_key=True)


# новая таблица - фотки и ролики машин и т.д.
class VehicleMedia(Base):
    __tablename__ = "vehicle_media"
    vehicle_id = Column(BigInteger, ForeignKey("vehicle.id"), primary_key=True)
    media_id = Column(BigInteger, ForeignKey("media.id"), primary_key=True)
    source_id = Column(BigInteger, ForeignKey("source.id"))


# ---- tables - таблицы
class Source(Base):
    __tablename__ = "source"
    id = Column(Integer, Sequence("source_id_seq"), primary_key=True)
    source_type = Column(Enum(SourceType))
    src = Column(Text)   # TODO: должны мы проверить длинность поля? зачем?

    def __repr__(self):
        return f"<Source(id={self.id}, src={self.src}>"


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, Sequence("person_id_seq"), primary_key=True)
    source_id = Column(BigInteger, ForeignKey("source.id"))
    source_type = Column(Enum(SourceType))
    external_id = Column(String(255))  # внешное ИД в источнике, если дано
    original_date_time = Column(DateTime)  # время в источнике
    parsing_date_time = Column(DateTime)  # время парсирования в источнике и добавления в базу данных

    # -- Полное имя, если не структурировано четко в ФИО
    full_name = Column(String(255))
    # -- Фамилия
    last_name = Column(String(100))
    # -- Имя или первая буква
    first_name = Column(String(100))
    # -- Отчество или первая буква
    middle_name = Column(String(100))

    # -- Пол
    gender = Column(Enum(Gender))
    # -- День рождения
    birth_date = Column(Date)
    # -- город, деревня и тд
    origin_place = Column(String(255))

    # -- гражданский номер
    identity_number = Column(String(32))
    # -- номер с серией, например AB123456
    passport_number = Column(String(50))
    passport_issue_date = Column(Date)
    passport_issue_place = Column(String(255))
    # нет змысла ограничать длинности поля, потому что в Narushitel.org иногда это поле очень длинные
    rank = Column(Text)

    # -- город, где человек был последний раз замечен
    last_known_location = Column(String(255))
    notes = Column(Text)

    media_items = relationship(
        "Media",
        secondary=PersonMedia.__table__,
        primaryjoin="PersonMedia.person_id==Person.id",
        secondaryjoin="PersonMedia.media_id==Media.id"
    )
    incidents = relationship("PersonIncident")
    types = relationship("PersonType", primaryjoin="Person.id==PersonType.person_id")
    personal_relations = relationship(
        "Person",
        secondary=PersonPerson.__table__,
        primaryjoin=PersonPerson.from_person_id == id,
        secondaryjoin=PersonPerson.to_person_id == id
    )
    addresses = relationship("Address")
    properties = relationship("Property")
    documents = relationship("Document", primaryjoin="Person.id==Document.owner_id")
    owned_vehicles = relationship("Vehicle", primaryjoin="Person.id==Vehicle.owner_id")
    used_vehicles = relationship("Vehicle", primaryjoin="Person.id==Vehicle.person_id")
    jobs = relationship("Job", primaryjoin="Person.id==Job.employee_id")
    social_networks = relationship("SocialNetwork")
    phones = relationship("Phone")
    emails = relationship("Email")

    def __repr__(self):
        return f"<Person(full_name={self.full_name}, birth_date={self.birth_date})>"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, Sequence("address_id_seq"), primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))

    # -- полный адрес, прочитанный из источника
    full_addr = Column(Text)
    address_type = Column(Enum(AddressType))
    position = Column(Geometry(geometry_type="POINT", srid=4326))

    country = Column(String(2))
    city = Column(String(100))

    # -- область
    region = Column(String(100))
    # -- Район
    district = Column(String(100))

    building = Column(String(100))
    block = Column(String(100))
    appartment = Column(String(100))

    from_date = Column(Date)
    to_date = Column(Date)
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Address(country={self.country}, city={self.city}, " \
               f"region={self.region}, full_addr={self.full_addr})>"


class Property(Base):
    __tablename__ = "property"
    id = Column(Integer, Sequence("property_id_seq"), primary_key=True)
    address = Column(BigInteger, ForeignKey("address.id"))
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))
    type = Column(String(50))
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Property(id={self.id}, type={self.type}>"


# все документы: паспорты, Водительское удостоверения, и т.д.
class Document(Base):
    __tablename__ = "document"
    id = Column(Integer, Sequence("document_id_seq"), primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))
    type = Column(String(50))  # TODO - сделать Enum-класс для этого типа
    title = Column(String(255))
    serial_number = Column(String(255))  # серия и номер документа
    valid_from = Column(Date)
    valid_to = Column(Date)
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Document(id={self.id}, type={self.type}, title={self.title}>"


class Vehicle(Base):
    __tablename__ = "vehicle"
    id = Column(Integer, Sequence("vehicle_id_seq"), primary_key=True)
    address_id = Column(BigInteger, ForeignKey("address.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    person_id = Column(BigInteger, ForeignKey("person.id"))

    type = Column(String(50))
    brand = Column(String(100))
    model = Column(String(100))
    license_plate = Column(String(10))
    color = Column(String(50))  # зачем такое большое поле? нет цветов с такими длинными названиями

    from_date = Column(Date)
    # -- Если по-прежнему используется, то to_date=null
    to_date = Column(Date)

    production_year = Column(SmallInteger)
    registration_year = Column(SmallInteger)
    vin = Column(String(50))
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Vehicle(type={self.type}, brand={self.brand}, model={self.model})>"


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, Sequence("organization_id_seq"), primary_key=True)
    address_id = Column(BigInteger, ForeignKey("address.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))

    name = Column(String(255))
    division = Column(String(255))

    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Organization(name={self.name}, division={self.division}, source_id={self.source_id})>"


class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, Sequence("job_id_seq"), primary_key=True)
    employer_id = Column(BigInteger, ForeignKey("organization.id"))
    employee_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))

    position = Column(Text)
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    from_date = Column(Date)
    # -- Если по-прежнему в силе, то to_date=null
    to_date = Column(Date)

    def __repr__(self):
        return f"<Job(position={self.position})>"


class SocialNetwork(Base):
    __tablename__ = "social_network"
    id = Column(Integer, Sequence("social_network_id_seq"), primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))

    # 10 - FB, 20 - VK.com, 30 - OK.ru 40 - Instagram, 50 - Telegram, 55 - другая
    # если будут другие сети, должно добавить числа для них, но пока их нет, использовать 55
    type = Column(Enum(SocialNetworkType))
    url = Column(String(255))
    net_name = Column(String(50))
    net_user_id = Column(String(255))
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<SocialNetwork(net_name={self.net_name}, net_id={self.net_id}, url={self.url})>"


class Phone(Base):
    __tablename__ = "phone"
    id = Column(Integer, Sequence("phone_id_seq"), primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))

    number = Column(String(255))
    normalized = Column(String(255))
    carrier = Column(String(100))

    from_date = Column(Date)
    # -- Если по-прежнему в силе, то to_date=null
    to_date = Column(Date)
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Phone(number={self.number}, normalized={self.normalized})>"


class Email(Base):
    __tablename__ = "email"
    id = Column(Integer, Sequence("email_id_seq"), primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))

    email = Column(String(255))
    from_date = Column(Date)
    # -- Если по-прежнему в силе, то to_date=null
    to_date = Column(Date)
    notes = Column(Text)

    def __repr__(self):
        return f"<Email(email={self.email}, notes={self.notes})>"


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, Sequence("media_id_seq"), primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("person.id"))
    source_id = Column(BigInteger, ForeignKey("source.id"))
    external_id = Column(String(255))  # внешное ИД в источнике, если дано

    type = Column(String(50))  # mime-type
    description = Column(Text)
    hash = Column(String(255))
    file_name = Column(String(255))
    size = Column(BigInteger)

    url = Column(Text)   # зачем полной URL в базе? дла "Нарушителя" сейчас я помещаю туда исходное имя файла
    original_url = Column(Text)
    created_at = Column(DateTime)  # timestamp
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Media(file_name={self.file_name}, external_id={self.external_id})>"


class Incident(Base):
    __tablename__ = "incident"
    id = Column(Integer, Sequence("incident_id_seq"), primary_key=True)
    source_id = Column(BigInteger, ForeignKey("source.id"))

    type = Column(String(50))
    name = Column(String(255))
    description = Column(Text)

    from_date_time = Column(DateTime)
    to_date_time = Column(DateTime)

    position = Column(Geometry(geometry_type="POINT", srid=4326))
    notes = Column(Text)  # Я бы не ограничивал длину текста 4096 символами, это может принести проблемы

    def __repr__(self):
        return f"<Incident(name={self.name}, type={self.type})>"


