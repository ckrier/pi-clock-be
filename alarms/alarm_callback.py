import random
import time
from os import listdir, path

from .alarm import Alarm
from ..db import db
from ..config import SOUND_FILE_DIR
from ..sounds.file_playback_client import FilePlaybackClient


def alarm_callback(alarm_id: str) -> None:
    with db.app.app_context():
        alarm = Alarm.query.get(alarm_id)

    current_volume = 0
    max_volume = 100
    fade_time_seconds = alarm.fadeInDuration * 60
    time_between_increment = fade_time_seconds / max_volume

    sound = random.choice(listdir(SOUND_FILE_DIR))
    player = FilePlaybackClient()

    player.set_volume(current_volume)
    player.set_sound(path.join(SOUND_FILE_DIR, sound))
    player.play()

    # increment volume by 1 in evenly spaced intervals
    while current_volume <= max_volume:
        current_volume += 1
        player.set_volume(current_volume)

        time.sleep(time_between_increment)
