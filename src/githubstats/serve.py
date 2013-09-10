from flask import Flask, render_template, send_from_directory
import os
import pymongo
from bson.json_util import dumps
import json
from githubstats import update_metrics
from flask.ext.pymongo import PyMongo
app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'metrics'
mongo = PyMongo(app, config_prefix='MONGO')

@app.route('/')
def custom_static():
    return send_from_directory(os.path.abspath('.'), 'index.html')

@app.route("/project/<path:package>")
def get_package(package):
    info = mongo.db.packages.find({"name": package})
    if info.count() < 1:
        return dumps({})
    else:
        return dumps(info[0])

@app.route("/scan_project/<path:package>")
def scan_package(package):
    info = mongo.db.packages.find({"name": package})
    update_metrics("/home/isaac/programming/yota/")
    return ""
    """
    if info.count() < 1:

    else:
        return json.dumps(info)
    """

if __name__ == "__main__":
    app.debug = True
    app.run()
