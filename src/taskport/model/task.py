from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

from taskport.model.when import When


@dataclass
class Name:
    v: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"))

    def __str__(self):
        return self.v


@dataclass
class Command:
    raw: str

    def __str__(self):
        return self.raw


@dataclass
class Tags:
    vs: List[str] = field(default_factory=list)

    def __str__(self):
        return ",".join(self.vs)

    def as_db_value(self) -> str:
        return ",%s," % self

    @classmethod
    def from_db_value(cls, v) -> 'Tags':
        return cls(list(filter(lambda x: x, v.split(",")[1:-1])))


@dataclass
class Task:
    cmd: Command
    name: Name = Name()
    tags: Tags = Tags()
    when: When = When.daily()

    def as_cron(self) -> str:
        suffix = "# taskport name: %s, tags: %s" % (self.name, self.tags)
        return "%s %s %s" % (self.when.as_cron(), self.cmd, suffix)

    def as_db_object(self) -> Dict[str, str]:
        return dict(
            cmd=str(self.cmd),
            name=str(self.name),
            tags=self.tags.as_db_value(),
            when=self.when.as_db_value()
        )

    @classmethod
    def from_db_object(cls, d) -> 'Task':
        return cls(cmd=Command(d['cmd']),
                   name=Name(d['name']),
                   tags=Tags.from_db_value(d['tags']),
                   when=When.from_db_value(d['when']))
