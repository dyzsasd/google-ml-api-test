import codecs
import json

from flask import Flask
import flask


app = Flask(__name__)
_ROOT_PATH = '/Users/s.zhang/workspace/dailymotion/google-ml-api/'

@app.route('/')
def index():
    return 'this is hello world.'

@app.route('/<string:dataset>')
def analysis_view(dataset):
    return flask.current_app.send_static_file('analysis.html')


@app.route('/api/<string:dataset>')
def analysis_result(dataset):
    try:
        with codecs.open(_ROOT_PATH + dataset, 'r', 'utf8') as fh:
            js = json.load(fh)
            return json.dumps(js)
    except:
        flask.abort(404)


if __name__ == '__main__':
    app.run()
