from flask import Flask, render_template, request, g, Response, redirect, session, abort, send_file, url_for
from flaskext.markdown import Markdown
from flask.ext.login import LoginManager, current_user
from jinja2 import FileSystemLoader, ChoiceLoader
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from shutil import rmtree, copyfile
from sqlalchemy import desc

import sys
import os
import subprocess
import urllib
import requests
import json
import zipfile
import locale
import traceback
import xml.etree.ElementTree as ET

from truecraft.config import _cfg, _cfgi
from truecraft.database import db, init_db
from truecraft.objects import User
from truecraft.common import *
from truecraft.network import *

from truecraft.blueprints.html import html
from truecraft.blueprints.legacy import legacy

app = Flask(__name__)
app.secret_key = _cfg("secret-key")
app.jinja_env.cache = None
app.jinja_env.filters['firstparagraph'] = firstparagraph
init_db()
login_manager = LoginManager()
login_manager.init_app(app)

Markdown(app)

@login_manager.user_loader
def load_user(username):
    return User.query.filter(User.username == username).first()

login_manager.anonymous_user = lambda: None

app.register_blueprint(html)
app.register_blueprint(legacy)

try:
    locale.setlocale(locale.LC_ALL, 'en_US')
except:
    pass

if not app.debug:
    @app.errorhandler(500)
    def handle_500(e):
        # shit
        try:
            db.rollback()
            db.close()
        except:
            # shit shit
            sys.exit(1)
        return render_template("internal_error.html"), 500
    # Error handler
    if _cfg("error-to") != "":
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler((_cfg("smtp-host"), _cfg("smtp-port")),
           _cfg("error-from"),
           [_cfg("error-to")],
           'truecraft.io application exception occured',
           credentials=(_cfg("smtp-user"), _cfg("smtp-password")))
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

@app.errorhandler(404)
def handle_404(e):
    return render_template("not_found.html"), 404

@app.before_request
def find_dnt():
    field = "Dnt"
    do_not_track = False
    if field in request.headers:
        do_not_track = True if request.headers[field] == "1" else False

    g.do_not_track = do_not_track

@app.context_processor
def inject():
    return {
        'root': _cfg("protocol") + "://" + _cfg("domain"),
        'domain': _cfg("domain"),
        'len': len,
        'any': any,
        'request': request,
        'locale': locale,
        'url_for': url_for,
        'user': current_user,
        'do_not_track': g.do_not_track
    }
