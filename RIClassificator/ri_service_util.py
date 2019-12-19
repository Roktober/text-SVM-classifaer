import json
import flask


def to_json(data):
    return json.dumps(data, ensure_ascii=False)


def validate_predict():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            'No JSON sent')
        return (None, errors)
    if not isinstance(json.get('values'), list) and isinstance(
            json.get('source'), int):
        errors.append('Values and source required')
        return (None, errors)
    return json, errors


def validate_add_data():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            'No JSON sent')
        return (None, errors)
    if not isinstance(
            json.get('values'),
            list) and not isinstance(
            json.get('classes'),
            list) and not isinstance(json.get('source'), int):
        errors.append('Values, classes, source required')
        return (None, errors)
    return json, errors


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype='application/json',
        response=to_json(data)
    )
