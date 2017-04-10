from flask import Flask
from flask import jsonify
import logging
import sync_airflow

app = Flask(__name__)


@app.route('/')
def hello():
    return "I'm the airflow syncer and I'm alive!\n"


@app.route('/sync')
def sync():
    return jsonify(sync_airflow.sync())


if __name__ == '__main__':
    # init logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.basicConfig()
    app.run(debug=True, host='0.0.0.0')