from flask import Flask, render_template, send_from_directory
import os
app = Flask(__name__)

client = pymongo.MongoClient('localhost')
db = client.metric_db
db.authenticate('guest', 'guest')

@app.route('/')
def custom_static():
    return send_from_directory(os.path.abspath('.'), 'index.html')

@app.route("/project/<path:package>")
def get_package(package):
    db.packages.find({"name": package},

if __name__ == "__main__":
    app.debug = True
    app.run()
