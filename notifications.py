import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

EMAIL_SUBJECT = "LEARN TO LEAD CLASSES AVAILABLE!"
EMAIL_BODY_GREETING = "Attention! The following \"Learn to Lead\" classes have been recently posted on the Urban Climb website:\n\n"
EMAIL_BODY_SIGNATURE = "\n\nRegards, PyFloyd"


def get_smtp_connection(
    smtp_server,
    smtp_user,
    smtp_password
):
    """Obtain a secured, authenticated SMTP connection."""
    s = smtplib.SMTP(smtp_server, 587)
    s.starttls(context = ssl.create_default_context())
    s.login(smtp_user, smtp_password)
    return s

def send_notification(
    connection,
    email_from: str,
    email_to: str,
    new_listings: tuple[str, str, str]
) -> None:
    """Sends a notification about new course listings to an address"""
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = EMAIL_SUBJECT

    body = EMAIL_BODY_GREETING \
            + "\n".join([f"{gym} - {month} - {dates}" for (gym, dates, month) in new_listings]) \
            + EMAIL_BODY_SIGNATURE
    msg.attach(MIMEText(body, 'plain'))

    connection.sendmail(email_from, email_to, msg.as_string())
