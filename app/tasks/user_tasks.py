from flask import render_template

from app.celery_worker import celery

from app.utils.email_utils import send_email


@celery.task()
def send_welcome_email(email):
    """
    Send welcome email.

    :param email: Recipient email
    """
    send_email('Welcome To RDoList.', [email],
               render_template('emails/texts/welcome_email.txt'),
               render_template('emails/welcome_email.html'))


@celery.task()
def send_verification_code_email(email, code):
    """
    Send verification code.

    :param email: User email
    :param code: Secret code
    """

    send_email('RDoList Verification Code.', [email],
               render_template('emails/texts/verification_code_email.txt',
                               code=code),
               render_template('emails/verification_code_email.html',
                               code=code))
