from dataclasses import dataclass, field
from datetime import datetime
from typing import List

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


@dataclass
class Task:
    cmd: Command
    name: Name = Name()
    tags: Tags = Tags()
    when: When = When.daily()

    def as_cron(self):
        suffix = "# taskport name: %s, tags: %s" % (self.name, self.tags)
        return "%s %s %s" % (self.when.as_cron(), self.cmd, suffix)
