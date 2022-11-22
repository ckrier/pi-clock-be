from http import HTTPStatus
from flask import Blueprint, jsonify, request, redirect

from .spotify_playback_client import pause, play, login

sound_controller = Blueprint('sounds', __name__, url_prefix='/sounds')


@sound_controller.route('/stop', methods=['PUT'])
def stopSound():
    pause()
    return '', HTTPStatus.NO_CONTENT


@sound_controller.route('/play', methods=['GET'])
def playSound():
    play()
    return '', HTTPStatus.NO_CONTENT


@sound_controller.route('/login', methods=['GET'])
def login_endpoint():
    return redirect(login(request.args.get("code")))
