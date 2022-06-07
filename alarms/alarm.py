from uuid import uuid4
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

    schedule = db.Column(
        db.Text,
        nullable=True
    )

    def __init__(self, id, hour, minute, schedule, enabled=False) -> None:
        super().__init__()

        if id is None:
            self.id = str(uuid4())
        else:
            self.id = id

        self.hour = hour
        self.minute = minute
        self.enabled = enabled

        if schedule is not None:
            self.schedule = ','.join(schedule)

    def toResponse(self):
        return {
            "id": self.id,
            "hour": self.hour,
            "minute": self.minute,
            "schedule": self.schedule if self.schedule is None else self.schedule.split(','),
            "enabled": self.enabled
        }

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __ne__(self, other):
        return self.hour != other.hour or self.minute != other.minute

    def __lt__(self, other):
        return self.hour <= other.hour and self.minute < other.minute
    
    def __le__(self, other):
        return self.hour <= other.hour and self.minute <= other.minute

    def __gt__(self, other):
        return self.hour >= other.hour and self.minute > other.minute

    def __ge__(self, other):
        return self.hour >= other.hour and self.minute > other.minute

    