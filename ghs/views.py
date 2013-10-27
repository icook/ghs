from flask import Blueprint, request, redirect, render_template, url_for, send_file, g, current_app, send_from_directory, abort, flash
from flask.ext.login import login_user, logout_user, current_user, login_required

from . import root, lm, app, oauth, github
from .models import User

import json
import mongoengine
import os
import sys
import base64


main = Blueprint('main', __name__, template_folder='../templates')


@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def user_loader(id):
    try:
        return User.objects.get(username=id)
    except User.DoesNotExist:
        pass

@main.errorhandler(403)
def access_denied(e):
    return render_template('403.html')

@main.route("/favicon.ico")
def favicon():
    return ""
    return send_file(os.path.join(root, 'static/favicon.ico'))

@main.route('/')
def home():
    return send_file(os.path.join(root, 'index.html'))

@app.route('/partials/<path:filename>')
def partials(filename):
    return send_file(os.path.join(root, 'partials', filename))

@app.route('/static/<path:filename>')
def static2(filename):
    return send_file(os.path.join(root, filename))

from .lib import catch_error_graceful
