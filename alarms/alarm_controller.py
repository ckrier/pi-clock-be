from http import HTTPStatus
from flask import Blueprint, jsonify, request

from ..db import db
from .alarm import Alarm
from .alarm_scheduler import AlarmScheduler

alarm_controller = Blueprint('alarms', __name__, url_prefix='/alarms')
alarm_scheduler = AlarmScheduler()


@alarm_controller.route('/', methods=['POST'])
def post_alarm():
    body = request.get_json(True)
    print(body)
    alarm = Alarm(None, body.get('hour', 0), body.get(
        'minute', 0), body.get('schedule', None))

    db.session.add(alarm)
    db.session.commit()

    return jsonify(alarm.toResponse()), HTTPStatus.CREATED


@alarm_controller.route('/', methods=['GET'])
def get_alarms():
    alarms = Alarm.query.all()
    alarms.sort()

    jsonAlarms = list(map(lambda a: a.toResponse(), alarms))
    return jsonify(jsonAlarms)


@alarm_controller.route('/<alarm_id>', methods=['GET'])
def get_alarm(alarm_id):
    alarm = Alarm.query.get(alarm_id)

    if alarm is None:
        return '', HTTPStatus.NOT_FOUND

    return jsonify(Alarm.query.get(alarm_id).toResponse())


@alarm_controller.route('/<alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
    alarm = Alarm.query.get(alarm_id)

    if alarm is None:
        return '', HTTPStatus.NOT_FOUND

    db.session.delete(alarm)
    db.session.commit()

    alarm_scheduler.disable(alarm.id)

    return '', HTTPStatus.NO_CONTENT


@alarm_controller.route('/<alarm_id>', methods=['PUT'])
def update_alarm(alarm_id):
    alarm = Alarm.query.get(alarm_id)
    body = request.get_json(True)

    if alarm is None:
        return '', HTTPStatus.NOT_FOUND

    alarm.hour = body.get('hour', 0)
    alarm.minute = body.get('minute', 0)
    alarm.enabled = body.get('enabled', False)
    alarm.schedule = body.get('schedule', None)

    db.session.commit()
    alarm_scheduler.schedule(alarm)

    return jsonify(alarm.toResponse())
