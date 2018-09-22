import os
from subprocess import CompletedProcess
from typing import Optional


def _prnt(msg):
    print(msg, flush=True)


class Logger:
    def __init__(self, logs_dir: str):
        os.makedirs(logs_dir, exist_ok=True)
        self._logs_dir = logs_dir

    def message(self, msg):
        _prnt(msg)

    def cmd_status(self, p: CompletedProcess, stdin: Optional[str]):
        _prnt("Command %s ended with status %d" % (p.args, p.returncode))
        _prnt("-Stdout-")
        for line in p.stdout.split("\n"):
            _prnt(line.rstrip())
        _prnt("-Stderr-")
        for line in p.stderr.split("\n"):
            _prnt(line.rstrip())
        if stdin:
            _prnt("-Stdin-")
            for line in stdin.split("\n"):
                _prnt(line.rstrip())
        _prnt("-End-")


_logger: Optional[Logger]


def loggy() -> Logger:
    assert _logger
    return _logger


def configure(logs_dir: str = "/tmp/taskport.logs"):
    global _logger
    _logger = Logger(logs_dir)

configure()
