import abc
import subprocess
from dataclasses import dataclass
from typing import List

from taskport.model.task import Task
from taskport.system.logging import loggy


class Device(abc.ABC):
    @abc.abstractmethod
    def install(self, tasks: List[Task]):
        pass

@dataclass
class CronInfo:
    cron_bin: str = "crontab"


class CronDevice(Device):
    def __init__(self, info: CronInfo):
        self._info = info

    def install(self, tasks: List[Task]):
        stuff = "\n".join([t.as_cron() for t in tasks]) + "\n"
#        noinspection PyArgumentList
        p = subprocess.run([self._info.cron_bin],input=stuff, capture_output=True, text=True)
        if p.returncode:
            loggy().cmd_status(p, stuff)
        p.check_returncode()
