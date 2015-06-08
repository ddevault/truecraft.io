from flask import Blueprint, abort, request, redirect, session, url_for
from flask.ext.login import current_user, login_user, logout_user
from truecraft.database import db
from truecraft.objects import *
from truecraft.common import *
from truecraft.config import _cfg

import os
import hashlib
import datetime

legacy = Blueprint('api', __name__, template_folder='../../templates')

@legacy.route("/api/login", methods=["POST"])
@with_session
def login():
    username = request.form.get('user')
    password = request.form.get('password')
    version = request.form.get('version')
    if not username or not password or not version:
        return "Missing username or password or launcher version parameters"
    if version != "12":
        return "Old Version"
    user = User.query.filter(User.username.ilike(username)).first()
    if not user:
        return "Invalid username or password"
    if bcrypt.checkpw(password, user.password):
        salt = os.urandom(40)
        user.sessionId = hashlib.sha256(salt).hexdigest()
        user.sessionExpiry = datetime.datetime.utcnow() + datetime.timedelta(minutes = 10)
        # first number doesn't really matter
        return "1281688214000:deprecated:{}:{}".format(user.username, user.sessionId)
    else:
        return "Invalid username or password"

@legacy.route("/session")
@with_session
def keep_alive():
    username = request.args.get('name')
    sessionId = request.args.get('session')
    if not username or not sessionId:
        return "Missing username or session parameters"
    user = User.query.filter(User.username.ilike(username)).first()
    if not user:
        return "Unknown user"
    if datetime.datetime.utcnow() > user.sessionExpiry:
        return "Session expired."
    if sessionId != user.sessionId:
        return "Invalid session key"
    return "Session renewed."
