import vlc

vlc_player = vlc.MediaPlayer('resources/mp3/water.mp3')


def play():
    vlc_player.play()


def pause():
    vlc_player.stop()


def stop():
    vlc_player.stop()


def is_playing():
    vlc_player.is_playing()


def login(code):
    pass
