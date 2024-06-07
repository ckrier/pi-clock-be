from uuid import uuid4
from sqlalchemy import orm, event
from ..db import db


class Alarm(db.Model):
    __tablename__ = 'alarms'

    id = db.Column(
        db.String(36),
        primary_key=True,
        nullable=False,
        unique=True
    )

    hour = db.Column(
        db.Integer,
        nullable=False,
    )

    minute = db.Column(
        db.Integer,
        nullable=False
    )

    enabled = db.Column(
        db.Boolean,
        nullable=False
    )

    # the amount of time it takes for an alarm to reach full volume in seconds
    fadeInDuration = db.Column(db.Integer, nullable=False)

    # don't use me. I'm only public to avoid inconveniences with the ORM event listeners
    internal_schedule = db.Column(
        'schedule',
        db.Text,
        nullable=True
    )

    schedule = None

    def __init__(self, id: str, hour: int, minute: int, schedule: str, enabled=False, fadeInDuration=0) -> None:
        super().__init__()

        if id is None:
            self.id = str(uuid4())
        else:
            self.id = id

        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.schedule = schedule
        self.fadeInDuration = fadeInDuration

        if schedule is not None:
            self.internal_schedule = ','.join(schedule)

    def toResponse(self):
        return {
            "id": self.id,
            "hour": self.hour,
            "minute": self.minute,
            "schedule": self.schedule,
            "enabled": self.enabled,
            "fadeInDuration": self.fadeInDuration
        }

    @orm.reconstructor
    def __reconstruct__(self):
        if self.internal_schedule is not None:
            self.schedule = self.internal_schedule.split(',')

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __ne__(self, other):
        return self.hour != other.hour or self.minute != other.minute

    def __lt__(self, other):
        if self.hour < other.hour:
            return True
        elif self.hour == other.hour and self.minute < other.minute:
            return True
        else:
            return False

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__lt__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


def decompressSchedule(target, context):
    if target.internal_schedule is not None:
        target.schedule = target.internal_schedule.split(',')


def compressSchedule(mapper, connection, target):
    if target.schedule is not None:
        target.internal_schedule = ','.join(target.schedule)
    else:
        target.internal_schedule = None


event.listen(Alarm, 'before_insert', compressSchedule)
event.listen(Alarm, 'before_update', compressSchedule)
event.listen(Alarm, 'load', decompressSchedule)
