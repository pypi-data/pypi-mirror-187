"""
data implementations that optionally uses joblib caching
"""

from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from io import BytesIO
from logging import info
from typing import List, Set
from zipfile import ZipFile

from pandas import read_csv
from pandera import check_types
from pandera.typing import DataFrame
from sqlmodel import Session

from .base import DayBase, MonthBase
from .concepts import Fuel, Timezone
from .config import DATE_START, TZ, YEAR_START
from .db import Database, DatabaseInMemory, File
from .db import Snapshot as SnapshotSQL
from .repository import Repository, RepositoryInMemory
from .schema import Snapshot


@dataclass
class Day:
    repo: Repository = RepositoryInMemory()
    db: Database = DatabaseInMemory()
    day_base: DayBase = DayBase.from_date(DATE_START)

    @property
    def last_modified(self) -> datetime:
        return max(self.repo.get_last_modifieds(self.month.month_base.name_file_zip))

    @cached_property
    def content(self) -> bytes:
        with BytesIO(
            self.repo.get(self.month.month_base.name_file_zip, self.last_modified)
        ) as f:
            with ZipFile(f) as zf:
                content = zf.read(self.day_base.name_file_csv)
        return content

    @property
    def month(self):  # -> Month
        return Month(month_base=MonthBase.from_date(self.day_base.dt), repo=self.repo)

    def extract(self) -> None:
        info(f"extracting daily csv for {self.day_base.dt.strftime('%Y/%m/%d')}")
        name = self.day_base.name_file_csv
        last_modified = self.last_modified
        if not self.repo.contains(
            name
        ) or last_modified not in self.repo.get_last_modifieds(name):
            self.repo.add(name=name, last_modified=last_modified, contents=self.content)

    @property  # type: ignore
    @check_types
    def df(self) -> DataFrame[Snapshot]:
        return (
            read_csv(BytesIO(self.content), dtype=object)
            .rename(columns={"Gen MWh": "Gen MW"})
            .assign(
                **{
                    Snapshot.timezone: lambda df: df[Snapshot.timezone].map(Timezone),
                    Snapshot.fuel: lambda df: df[Snapshot.fuel].map(Fuel),
                }
            )
        )

    def snapshots(self, file_id: int) -> list[SnapshotSQL]:
        return [
            SnapshotSQL(**info, file_id=file_id)
            for info in self.df.to_dict(orient="records")
        ]

    @property
    def file(self) -> File:
        return File(name=self.day_base.name_file_csv, last_modified=self.last_modified)

    def load(self) -> None:
        info(f"loading snapshots to db {self.db} for day {self.day_base.dt}...")
        id = self.db.add_file(self.file)
        try:
            self.db.add_snapshots(self.snapshots(id))
        except Exception as e:
            info("...could not load snapshots.")
            self.db.rm_file(self.file)
            raise e
        info("...loading snapshots done.")


@dataclass
class Month:
    repo: Repository = RepositoryInMemory()
    db: Database = DatabaseInMemory()
    month_base: MonthBase = MonthBase.from_date(DATE_START)

    @property
    def days(self) -> List[Day]:
        days = []
        current = DayBase.from_date(dt=self.month_base.dt)
        while current.yearmonth == self.month_base:
            if not current.is_before_start and not current.is_future:
                days.append(current)
            current = current.next
        return [Day(day_base=day, repo=self.repo, db=self.db) for day in days]

    def pull(self) -> None:
        info(f"pulling zip for month {self.month_base.year}/{self.month_base.month}")
        name = self.month_base.name_file_zip
        last_modified = self.month_base.last_modified
        if not self.repo.contains(
            name
        ) or last_modified not in self.repo.get_last_modifieds(name):
            self.repo.add(
                name=name, last_modified=last_modified, contents=self.month_base.zip
            )

    def extract(self) -> None:
        info(
            f"extracting daily csvs for month {self.month_base.year}/{self.month_base.month}"
        )
        for day in self.days:
            day.extract()

    def load(self) -> None:
        info(
            f"loading daily csvs into db for month {self.month_base.year}/{self.month_base.month}"
        )
        for day in self.days:
            if not self.db.has_file(day.file):
                day.load()


@dataclass
class Year:
    repo: Repository = RepositoryInMemory()
    db: Database = DatabaseInMemory()
    year: int = YEAR_START

    @property
    def months(self) -> List[Month]:
        return [
            Month(repo=self.repo, db=self.db, month_base=month)
            for month in [
                MonthBase(year=self.year, month=month) for month in range(1, 13)
            ]
            if not month.is_future and not month.is_before_start
        ]

    def pull(self) -> None:
        info(f"pulling monthly zips for year {self.year}")
        for month in self.months:
            month.pull()

    def extract(self) -> None:
        info(f"extracting daily csvs for year {self.year}")
        for month in self.months:
            month.extract()

    def load(self) -> None:
        info(f"loading daily csvs into db for year {self.year}")
        for month in self.months:
            month.load()


@dataclass
class All:
    repo: Repository = RepositoryInMemory()
    db: Database = DatabaseInMemory()

    @property
    def years(self) -> List[Year]:
        now = datetime.now(TZ)
        return [
            Year(repo=self.repo, db=self.db, year=year)
            for year in range(YEAR_START, now.year + 1)
        ]

    def pull(self) -> None:
        info("pulling monthly zips from all years")
        for year in self.years:
            year.pull()

    def extract(self) -> None:
        info("extracting daily csvs from all years")
        for year in self.years:
            year.extract()

    def load(self) -> None:
        info("loading daily csvs into db from all years")
        for year in self.years:
            year.load()
