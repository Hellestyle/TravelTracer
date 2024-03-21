from flask import render_template
from flask_mail import Mail, Message

import config.email


def send_email(app, recipients, subject, html):

    mail = Mail(app)

    message = Message(
        subject, sender=('TravelTracer', config.email.MAIL_USERNAME),
        recipients=recipients
    )
    
    message.html = html

    with app.app_context():
        mail.send(message)