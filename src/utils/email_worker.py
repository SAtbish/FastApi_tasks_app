import smtplib
from email.message import EmailMessage

from config import EMAIL_SENDER, SMTP_PASSWORD
from src.schemas.notifications import NotificationRedisModel

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


async def send_message_to_email(notification: NotificationRedisModel, user_email: str):
    message = EmailMessage()
    message['Subject'] = notification.header
    message['From'] = EMAIL_SENDER
    message['To'] = user_email

    message.set_content(
        notification.message,
        subtype='html'
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp_connection:
        smtp_connection.starttls()
        smtp_connection.login(EMAIL_SENDER, SMTP_PASSWORD)
        smtp_connection.sendmail(EMAIL_SENDER, user_email, message.as_string())
