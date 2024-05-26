import random
import time
from os import listdir, path
from ..config import SOUND_FILE_DIR
from ..sounds.file_playback_client import FilePlaybackClient


def alarm_callback():
    current_volume = 0
    max_volume = 100
    fade_time_seconds = 15 * 60
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
