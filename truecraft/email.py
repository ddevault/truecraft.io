import smtplib
import pystache
import os
import html.parser
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from flask import url_for

from truecraft.database import db
from truecraft.objects import User
from truecraft.config import _cfg, _cfgi

def send_confirmation(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/confirm-account") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), { 'user': user, "domain": _cfg("domain"), 'confirmation': user.confirmation })))
    message['X-MC-Important'] = "true"
    message['X-MC-PreserveRecipients'] = "false"
    message['Subject'] = "Confirm your TrueCraft account"
    message['From'] = "mailer@knightos.org"
    message['To'] = user.email
    smtp.sendmail("mailer@truecraft.io", [ user.email ], message.as_string())
    smtp.quit()
