from http import HTTPStatus
from flask import Blueprint, jsonify, request

from .spotify_playback_client import pause

sound_controller = Blueprint('sounds', __name__, url_prefix='/sounds')


@sound_controller.route('/stop', methods=['PUT'])
def stopSound():
    pause()
    return '', HTTPStatus.NO_CONTENT
