from time import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger

from ..sounds.spotify_playback_client import play
from ..config import SQLALCHEMY_DATABASE_URI


def fu():
    print("Alarm Triggered")


class AlarmScheduler:
    __jobstores = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }

    __executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }

    __job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }

    __scheduler = None

    def __init__(self):
        scheduler = BackgroundScheduler(
            jobstores=self.__jobstores, executors=self.__executors, job_defaults=self.__job_defaults)

        scheduler.start()
        self.__scheduler = scheduler

    def schedule(self, alarm):
        if alarm is None:
            return

        if alarm.enabled:
            self.__scheduler.add_job(
                func=play,
                trigger=self.__create_cron_trigger__(alarm),
                id=alarm.id,
                replace_existing=True)
        else:
            self.disable(alarm.id)

    def disable(self, alarm_id):
        if alarm_id is None or self.__scheduler.get_job(alarm_id) is None:
            return

        self.__scheduler.remove_job(alarm_id)

    def __create_cron_trigger__(self, alarm):
        cron_days = list(map(lambda day: day[:3], alarm.schedule or []))
        cron_expr = ','.join(cron_days) if len(cron_days) > 0 else None
        return CronTrigger(hour=alarm.hour, minute=alarm.minute, day_of_week=cron_expr)
