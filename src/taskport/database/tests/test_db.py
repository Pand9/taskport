import os
import unittest

import pytest

from taskport.database.db import SqliteDB
from taskport.model.task import Task, Name, Command, Tags


class TestDB:

    @pytest.fixture
    def db(self):
        os.remove("/tmp/taskport.db")
        return SqliteDB("/tmp/taskport.db")

    def test_empty(self, db):
        assert db.all() == []

    def test_add(self, db):
        db.add(Task(Command("cmd"), Name("name")))
        assert db.all() == [Task(Command("cmd"), Name("name"))]

    def test_get(self, db):
        db.add(Task(Command("cmd"), Name("name1")))
        db.add(Task(Command("cmd"), Name("name2")))
        assert db.get(Name("dummy")) is None
        assert db.get(Name("name1")) == Task(Command("cmd"), Name("name1"))
        assert db.get(Name("name2")) == Task(Command("cmd"), Name("name2"))

    def test_delete(self, db):
        db.add(Task(Command("cmd"), Name("name1")))
        db.add(Task(Command("cmd"), Name("name2")))
        db.delete(Name("name1"))
        assert db.get(Name("name1")) is None
        assert db.get(Name("name2"))

    def test_add_second(self, db):
        assert db.add(Task(Command("cmd"), Name("name"))) is True
        assert db.add(Task(Command("cmd"), Name("name"))) is False

    def test_find(self, db):
        db.add(Task(Command("cmd"), Name("name1"), Tags(["tag1", "tag2"])))
        db.add(Task(Command("cmd"), Name("name2"), Tags(["tag2", "tag3"])))
        assert len(db.find("tag1")) == 1
        assert len(db.find("tag2")) == 2
        assert len(db.find("tag3")) == 1
        assert len(db.find("tag4")) == 0
