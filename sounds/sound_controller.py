from http import HTTPStatus
from flask import Blueprint, request, redirect

from ..sounds.file_playback_client import FilePlaybackClient

sound_controller = Blueprint('sounds', __name__, url_prefix='/sounds')
player = FilePlaybackClient()


@sound_controller.route('/stop', methods=['PUT'])
def stopSound():
    player.pause()
    return '', HTTPStatus.NO_CONTENT


@sound_controller.route('/play', methods=['GET'])
def playSound():
    player.play()
    return '', HTTPStatus.NO_CONTENT


# @sound_controller.route('/login', methods=['GET'])
# def login_endpoint():
#     return redirect(login(request.args.get("code")))
