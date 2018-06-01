from flask_mail import Message
from app.extensions import mail

from app.celery_worker import celery


@celery.task()
def send_email(subject, recipients, text_body, html_body, sender=None):
    """
    Send email with Flask-Mail.

    :param subject: Email subject
    :param recipients: Email recipients.
    :param text_body: Email raw text
    :param html_body: Email html
    :param sender: Authority name
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    mail.send(msg)
