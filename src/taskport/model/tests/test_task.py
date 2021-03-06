from taskport.model.task import Task, Command, Name, Tags
from taskport.model.when import When


class TestsTask:
    def test_task_definition(self):
        task = Task(Command("echo tete a tete"))
        assert """0 0 * * * /bin/bash -c "echo tete a tete; echo 'taskport""" in task.as_cron()
        task = Task(cmd=Command("echo heh"),
                    name=Name("yolo"),
                    tags=Tags(["tag1", "tag2"]),
                    when=When.daily(13, 24))
        assert '''24 13 * * * /bin/bash -c "echo heh; echo 'taskport name: yolo, tags: tag1,tag2'"''' == task.as_cron()

