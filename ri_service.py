import flask
from RIClassificator import RIClassificator
import json
from Data import Data
from get_data import from_csv
from test import test_all


def to_json(data):
    return json.dumps(data, ensure_ascii=False)


def validate_preprocess():
    errors = []
    json = flask.request.args.get('string')
    if json is None:
        errors.append(
            'Param string reqired')
        return (None, errors)
    return json, errors


def validate_predict():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            'No JSON sent')
        return (None, errors)
    if not isinstance(json.get('values'), list):
        errors.append('Values required')
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
            list):
        errors.append('Values and classes required')
        return (None, errors)
    return json, errors


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype='application/json',
        response=to_json(data)
    )


test_all()

app = flask.Flask(__name__)

data = Data()
classificator = RIClassificator(data)


@app.route('/ri_classificator/predict', methods=['POST'])
def predict():
    """
    curl -XPOST -H 'Content-Type: application/json' -d '{"ids": [1,2,3,4,5], "values":["аниме", "гараж", "аниме", "гираж", "аниме"]}' 'localhost:8080/matching/classification/predict'
    """
    try:
        (json, errors) = validate_predict()

        if errors:
            return resp(400, {'errors': errors})

        val = json.get('values')
        clss = classificator.predict(val)
        return resp(200, {'classes': clss})

    except Exception as e:
        print(e)
        return resp(500, {})


@app.route('/ri_classificator/classes', methods=['GET'])
def get_classes():
    try:
        clss = classificator.data.classes_name
        return resp(200, {'classes': clss})
    except Exception as e:
        print(e)
        return resp(500, {})


@app.route('/ri_classificator/add_data', methods=['POST'])
def add_data():
    """
    curl -XPOST -H 'Content-Type: application/json' -d '{"ids": [1,2,3,4], "values":["аниме", "гараж", "аниме", "гираж", "аниме"],"classes":["аниме", "гараж", "аниме", "гараж", "аниме"]}'   'localhost:8080/matching/classification/add_data'
    """
    try:
        (json, errors) = validate_add_data()
        if errors:
            print(errors)
            return resp(400, {'errors': errors})

        val, clss = json.get('values'), json.get('classes')
        print(val, clss)
        check_clss = set(clss)
        new_classes = []
        for cl in check_clss:
            if cl not in classificator.data.classes_name:
                new_classes.append(cl)
        if new_classes:
            classificator.add_classes(new_classes)
        classificator.add_data_with_preprocessing(val, clss)
        return resp(200, {})
    except Exception as e:
        print(e)
        return resp(500, {})


@app.route('/ri_classificator/ready', methods=['GET'])
def ready():
    try:
        if classificator.data.classes_name and classificator.data.document_data:
            return resp(200, 1)
        else:
            return resp(200, 0)
    except Exception as e:
        print(e)
        return resp(500, {})


@app.route('/ri_classificator/preprocess_string', methods=['GET'])
def preprocess_string():
    try:
        data, errors = validate_preprocess()
        if errors:
            return resp(400, {'errors': errors})
        preprocess_string = classificator.preprocess_text([data])
        return resp(200, preprocess_string[0])
    except Exception as e:
        print(e)
        return resp(500, {})


if __name__ == '__main__':
    app.debug = False
    app.run(port=5000)
