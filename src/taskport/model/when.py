from dataclasses import dataclass


@dataclass
class When:
    raw: str

    @classmethod
    def daily(cls, hour: int = 0, minute: int = 0):
        return cls("%d %d * * *" % (minute, hour))

    def as_cron(self):
        return self.raw

    def as_db_value(self):
        return self.raw

    @classmethod
    def from_db_value(cls, v) -> 'When':
        return cls(v)
