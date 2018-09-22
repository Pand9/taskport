import os
import time

from taskport.model.task import Task, Name, Command, Tags
from taskport.model.when import When
from taskport.runner.device import CronInfo, CronDevice


class TestDevice:
    def test_install(self):
        d = CronDevice(CronInfo())
        n = "/tmp/test.taskport.device.install.guard"
        if os.path.isfile(n):
            os.remove(n)
        assert not os.path.isfile(n)
        d.install([Task(
            name=Name("me"),
            cmd=Command(f"echo qq > {n}"),
            when=When("* * * * *"),
            tags=Tags(["tag1, tag2"])
        )])
        time.sleep(60)
        d.install([])
        assert os.path.isfile(n)
        os.remove(n)
        time.sleep(62)
        assert not os.path.isfile(n)


if __name__ == "__main__":
    TestDevice().test_install()
