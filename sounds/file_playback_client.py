from vlc import MediaList, MediaListPlayer, PlaybackMode


class FilePlaybackClient:
    __player = None
    __sound = 'resources/mp3/water.mp3'

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FilePlaybackClient, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        player = MediaListPlayer()
        player.set_media_list(MediaList([self.__sound]))
        player.set_playback_mode(PlaybackMode.loop)

        self.__player = player

    def play(self):
        self.__player.play()

    def pause(self):
        self.__player.stop()

    def stop(self):
        self.__player.stop()

    def is_playing(self):
        self.__player.is_playing()

    def set_sound(self, sound):
        if sound is not None:
            self.__player.set_media_list(MediaList([sound]))

    def set_volume(self, amount):
        if amount > 100:
            amount = 100
        elif amount < 0:
            amount = 0

        self.__player.audio_set_volume(amount)
