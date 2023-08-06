"""
Tools for managing fuel mix monthly zips and daily csvs from NYISO 
"""

from abc import ABC, abstractmethod
from datetime import datetime
from logging import info
from pickle import dumps, loads

from fs_gcsfs import GCSFS

from .settings import SettingsGCS


class Repository(ABC):
    @abstractmethod
    def add(self, name: str, last_modified: datetime, contents: bytes) -> None:
        pass

    @abstractmethod
    def contains(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_last_modifieds(self, name: str) -> set[datetime]:
        pass

    @abstractmethod
    def get(self, name: str, last_modified: datetime) -> bytes:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


class RepositoryInMemory(Repository):
    def __init__(self):
        self.last_modifieds: dict[str, set[datetime]] = {}
        self.contents: dict[tuple(str, datetime), bytes] = {}

    def add(self, name: str, last_modified: datetime, contents: bytes) -> None:
        if self.contains(name):
            self.last_modifieds[name].add(last_modified)
        else:
            self.last_modifieds[name] = {last_modified}
        self.contents[(name, last_modified)] = contents

    def contains(self, name: str) -> bool:
        return name in self.last_modifieds.keys()

    def get_last_modifieds(self, name: str) -> set[datetime]:
        return self.last_modifieds[name]

    def get(self, name: str, last_modified: datetime) -> bytes:
        return self.contents[(name, last_modified)]

    def clear(self) -> None:
        pass


class RepositoryGCS(Repository):
    def __init__(self, name_bucket: str = SettingsGCS().name_bucket, prefix: str = ""):
        self.fs = GCSFS(name_bucket)
        self.prefix = prefix
        self.name_file_last_modifieds = f"{self.prefix}last_modifieds"
        self.last_modifieds: dict[str, set[datetime]] = (
            loads(self.get_from_name(self.name_file_last_modifieds))
            if self.fs.isfile(self.name_file_last_modifieds)
            else {}
        )

    def add_to_name(self, name: str, contents: bytes) -> None:
        info(f"adding to repo {self}: {name}")
        with self.fs.open(name, "wb") as f:
            f.write(contents)

    def name(self, name: str, last_modified: datetime) -> str:
        return f"{self.prefix}{last_modified.strftime('%Y%m%d_%H%M%S')}_{name}"

    def add(self, name: str, last_modified: datetime, contents: bytes) -> None:
        if name in self.last_modifieds.keys():
            self.last_modifieds[name].add(last_modified)
        else:
            self.last_modifieds[name] = {last_modified}
        self.add_to_name(self.name_file_last_modifieds, dumps(self.last_modifieds))
        self.add_to_name(self.name(name, last_modified), contents)

    def contains(self, name: str) -> bool:
        return name in self.last_modifieds.keys()

    def get_last_modifieds(self, name: str) -> set[datetime]:
        return self.last_modifieds[name]

    def get_from_name(self, name: str) -> bytes:
        info(f"grabbing from repo {self}: {name}")
        with self.fs.open(name, "rb") as f:
            content = f.read()
        return content

    def get(self, name: str, last_modified: datetime) -> bytes:
        return self.get_from_name(self.name(name, last_modified))

    def remove(self, name: str) -> None:
        info(f"removing from repo {self}: {name}")
        self.fs.remove(name)

    def clear(self) -> None:
        for name, dts in self.last_modifieds.items():
            for dt in dts:
                self.remove(self.name(name, dt))
        self.remove(self.name_file_last_modifieds)
        self.last_modifieds = {}
