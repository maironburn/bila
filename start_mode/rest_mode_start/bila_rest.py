from flask import Flask
from flask_restful import Api
from src.controllers.winmapper import WinMapper
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'jola'


@app.route('/main', methods=['GET'])
def main_window():
    winmaper = WinMapper({'current': 'main_window'})
    return json.dumps(winmaper.pantalla, sort_keys=True, indent=4)


api = Api(app)
if __name__ == '__main__':
    app.run(debug=True)
