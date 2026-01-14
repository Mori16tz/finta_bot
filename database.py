import datetime
from enum import StrEnum

from sqlalchemy import Enum, create_engine
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            sessionmaker)

Base = declarative_base()


class Vorlesung(StrEnum):
    KDI = "KDI"
    RSN = "RSN"
    DML = "DML"
    PK1 = "PK1"
    KDP = "KDP"
    SuG = "SuG"
    Anatomie = "Anatomie"


class Datenbank(Base):
    __tablename__ = "Datenbank"

    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    gesamt: Mapped[int]
    finta: Mapped[int]
    quote: Mapped[float]
    fach: Mapped[Vorlesung] = mapped_column(
        Enum(Vorlesung, native_enum=False), primary_key=True)
    nummer: Mapped[int]


engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_table() -> None:
    Base.metadata.create_all(
        engine, Base.metadata.tables.values(), checkfirst=True)


def get_quote(fach: Vorlesung) -> list[Datenbank]:
    return session.query(Datenbank).filter(Datenbank.Vorlesung == fach).all()


def add_entry(fach: Vorlesung, ges: str, finta: str, num: str, date_=datetime.date.today()) -> None:
    eintrag = Datenbank(date=date_, gesamt=int(
        ges), finta=int(finta), quote=round((int(finta)/int(ges))*100, 2), fach=fach, nummer=int(num))
    session.add(eintrag)
    session.commit()


def delete_entry(fach: Vorlesung, date: datetime.date) -> None:
    session.query(Datenbank).filter(Datenbank.fach ==
                                    fach, Datenbank.date == date).delete()
    session.commit()


def get_entry(fach: Vorlesung, date: datetime.date) -> Datenbank:
    return session.query(Datenbank).filter(Datenbank.fach == fach, Datenbank.date == date).first()
