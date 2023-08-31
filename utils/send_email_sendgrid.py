import os

from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, message, to_email):
    sg = SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)
    from_email = settings.DEFAULT_FROM_EMAIL
    
    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=message
    )
    
    try:
        response = sg.send(mail)
        return response.status_code
    except Exception as e:
        return e.message
