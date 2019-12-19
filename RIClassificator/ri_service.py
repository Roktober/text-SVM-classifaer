import flask
from RIClassificator import RIClassificator
import json
from Data import Data
from ClassificatorDAO import ClassificatorDAO
from test_classifaer import test_ri_classificator
from load_config import get_config_for_section
from ri_service_util import resp, to_json, validate_predict, validate_add_data
import logging


# Init config and logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d — %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            'app.log',
            mode='a',
            encoding='utf-8')])
config = get_config_for_section('FLASK')
port = int(config['port'])
host = config['host']

# Test classifaer
test_ri_classificator()

# Init Flask app
app = flask.Flask(__name__)


classificatorDAO = ClassificatorDAO()
data = Data()
classificator = RIClassificator(data, classificatorDAO)


@app.route('/ri_classificator/predict', methods=['POST'])
def predict():
    try:
        (json, errors) = validate_predict()
        if errors:
            return resp(400, {'errors': errors})

        val, source = json.get('values'), json.get('source')
        clss = classificator.predict(val, source)
        return resp(200, {'classes': clss})

    except Exception as e:
        logging.info(f'error in predict: {e}')
        return resp(500, {})


@app.route('/ri_classificator/add_data', methods=['POST'])
def add_data():
    try:
        (json, errors) = validate_add_data()
        if errors:
            print(errors)
            return resp(400, {'errors': errors})

        val, clss, source = json.get('values'), json.get(
            'classes'), json.get('source')
        classificator.add_data(val, clss, source)
        return resp(200, {})
    except Exception as e:
        logging.info(f'error in add_data: {e}')
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


if __name__ == '__main__':
    app.debug = False
    app.run(host=host, port=port)
