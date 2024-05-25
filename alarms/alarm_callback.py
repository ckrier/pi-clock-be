import random
from os import listdir, path
from ..config import SOUND_FILE_DIR
from ..sounds.file_playback_client import FilePlaybackClient


def alarm_callback():
    sound = random.choice(listdir(SOUND_FILE_DIR))

    player = FilePlaybackClient()
    player.set_sound(path.join(SOUND_FILE_DIR, sound))
    player.play()
