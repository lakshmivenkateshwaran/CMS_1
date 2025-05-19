import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List
from config.email_config import settings

MAIL_USERNAME = settings.MAIL_USERNAME
MAIL_PASSWORD = settings.MAIL_PASSWORD
MAIL_FROM = settings.MAIL_FROM
MAIL_FROM_NAME = settings.MAIL_FROM_NAME
MAIL_SERVER = settings.MAIL_SERVER
MAIL_PORT = settings.MAIL_PORT

def send_email_report(subject, recipient_emails, report_name, table_html):
    msg = MIMEMultipart()
    msg['From'] = f"{MAIL_FROM_NAME} <{MAIL_USERNAME}>"
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject

    body = f"""
    <html>
        <body>
            <p>Here is your shared report: <b>{report_name}</b></p>
            {table_html}
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_FROM, recipient_emails, msg.as_string())