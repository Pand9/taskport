import abc
import logging
from typing import Optional, List

from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey

from taskport.model.task import Task, Name


class DB(abc.ABC):
    @abc.abstractmethod
    def add(self, task: Task) -> Optional[Name]:
        pass

    @abc.abstractmethod
    def get(self, name: Name) -> Optional[Task]:
        pass

    @abc.abstractmethod
    def delete(self, name: Name) -> None:
        pass

    @abc.abstractmethod
    def find(self, tag: str) -> List[Task]:
        pass

    @abc.abstractmethod
    def all(self) -> List[Task]:
        pass


class SqliteDB(DB):
    def __init__(self, db_path):
        self._eng = create_engine(f"sqlite:///{db_path}")
        self._md = MetaData(bind=self._eng)
        self._tasks = Table("task", self._md,
                            Column("cmd", String),
                            Column("name", String,
                                   primary_key=True),
                            Column("tags", String),
                            Column("when", String))

        self._md.create_all()

    def add(self, task: Task) -> bool:
        if self.get(task.name):
            return False
        self._eng.execute(self._tasks.insert(task.as_db_object()))
        return True

    def get(self, name: Name) -> Optional[Task]:
        vals = list(self._eng.execute(self._tasks.select().where(self._tasks.c.name == str(name))))
        return Task.from_db_object(vals[0]) if vals else None

    def delete(self, name: Name) -> None:
        self._eng.execute(self._tasks.delete().where(self._tasks.c.name == str(name)))

    def find(self, tag: str) -> List[Task]:
        vals = self._eng.execute(self._tasks.select().where(self._tasks.c.tags.like('%,' + tag + ",%")))
        return [Task.from_db_object(v) for v in vals]

    def all(self) -> List[Task]:
        vals = self._eng.execute(self._tasks.select())
        return [Task.from_db_object(v) for v in vals]
