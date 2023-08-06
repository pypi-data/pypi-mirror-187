"""
Tools for working with the fuel mix data in a database
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Enum
from sqlalchemy.future import Engine
from sqlmodel import Field, SQLModel, create_engine, Session, select

from nysmix.concepts import Fuel, Timezone

from .settings import SettingsPostgres
from logging import info


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    last_modified: datetime


class Snapshot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(alias="Time Stamp")
    timezone: Timezone = Field(alias="Time Zone", sa_column=Column(Enum(Timezone)))
    fuel: Fuel = Field(alias="Fuel Category", sa_column=Column(Enum(Fuel)))
    gen_mw: float = Field(alias="Gen MW")

    file_id: Optional[int] = Field(default=None, foreign_key="file.id")

    class Config:
        allow_population_by_field_name = True


class Database(ABC):
    engine: Engine

    def create(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def add_file(self, file: File) -> int:
        with Session(self.engine) as session:
            info(f"loading file {file}...")
            session.add(file)
            session.commit()
            id = file.id
            assert id is not None
            info(f"...loaded with id {id}.")
            return id

    def has_file(self, file: File) -> bool:
        with Session(self.engine) as session:
            num_files = (
                session.query(File)
                .filter(
                    (File.name == file.name)
                    & (File.last_modified == file.last_modified)
                )
                .count()
            )
        return num_files > 0

    def rm_file(self, file: File) -> None:
        if not self.has_file(file):
            return
        info(f"removing file {file}...")
        with Session(self.engine) as session:
            statement = select(File).where(
                (File.name == file.name) & (File.last_modified == file.last_modified)
            )
            results = session.exec(statement)
            file = results.one()
            session.delete(file)
            session.commit()
            info(f"...removed.")

    def add_snapshots(self, snapshots: list[Snapshot]) -> None:
        with Session(self.engine) as session:
            info("loading snapshots...")
            session.add_all(snapshots)
            session.commit()
            info("...loaded.")

    # @property
    # def max_id(self) -> int:
    #     with Session(self.engine) as session:
    #         max_id = session.query(func.max(Snapshot.id)).scalar()
    #     return max_id or 0


class DatabaseInMemory(Database):
    def __init__(self):
        self.engine = create_engine("sqlite://")


class DatabasePostgres(Database):
    def __init__(self, settings: Optional[SettingsPostgres] = None):
        self.settings = settings if settings else SettingsPostgres()
        self.engine = create_engine(
            self.settings.dsn,
            echo=True,
        )
