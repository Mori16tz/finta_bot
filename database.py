import datetime
from enum import StrEnum

from sqlalchemy import Enum, create_engine
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            sessionmaker)

Base = declarative_base()


class Lecture(StrEnum):
    KDI = "Konzepte der Informatik"
    RSN = "Rechnersysteme und -Netze"
    DML = "Diskrete Mathematik und Logik"
    PK1 = "Programmierkurs 1"
    KDP = "Konzepte der Programmierung"
    SuG = "Sport und Gesellschaft"
    Anatomie = "Anatomie"


class Database(Base):
    __tablename__ = "Database"

    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    total: Mapped[int]
    finta: Mapped[int]
    quota: Mapped[float]
    lecture: Mapped[Lecture] = mapped_column(
        Enum(Lecture, native_enum=False), primary_key=True)
    number: Mapped[int]


engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_table() -> None:
    Base.metadata.create_all(
        engine, Base.metadata.tables.values(), checkfirst=True)


def get_lecture(lecture: Lecture) -> list[Database]:
    return session.query(Database).filter(Database.lecture == lecture).all()


def add_entry(lecture: Lecture, ges: str, finta: str, num: str, date_=datetime.date.today()) -> None:
    eintrag = Database(date=date_, total=int(
        ges), finta=int(finta), quota=round((int(finta)/int(ges))*100, 2), lecture=lecture, number=int(num))
    session.add(eintrag)
    session.commit()


def delete_entry(lecture: Lecture, date: datetime.date) -> None:
    session.query(Database).filter(Database.lecture ==
                                    lecture, Database.date == date).delete()
    session.commit()


def get_entry(lecture: Lecture, date: datetime.date) -> Database:
    return session.query(Database).filter(Database.lecture == lecture, Database.date == date).first()
