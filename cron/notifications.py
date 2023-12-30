import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader

import constants as c
from config import parse_config
from model.notification import Notification

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

config = parse_config('PROJECTNAME.conf')
CFG = config['smtp']
SENDER = config['notifications']['sender']
SERVER = config['notifications']['server']
PREFIX = config['paths']['url_prefix']

j2env = Environment(loader=FileSystemLoader(config['paths']['templates']))


def send_html_email(subject, body, recipient):
    """With this function we send out our HTML email"""

    # Create message object
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['To'] = recipient
    message['From'] = SENDER
    message.preamble = """This email was sent in an HTML format.  Your mail reader does not support an HTML email format.
"""

    # set the MIME type to text/html.
    # and attach it as the last part of the message.
    # re: RFC 2046
    html_body = MIMEText(body, 'html')
    message.attach(html_body)

    with smtplib.SMTP_SSL(CFG['smtp_ssl_server'], CFG['smtp_port']) as s:
        try:
            # Debug: s.set_debuglevel(1)
            s.login(CFG['smtp_user'], CFG['smtp_password'])
            s.send_message(message)
        except smtplib.SMTPRecipientsRefused:
            pass  # don't fail, process the reset, admin will be notified


subjects = {
    c.FORGOT: "PROJECTNAME: Forgotten Password Code",
}


def notifications():
    engine = create_engine(config['db']['url'], echo=True)
    session = sessionmaker(bind=engine)()

    # TODO: Log emails that are processed
    n10ns = session.query(Notification).filter(Notification.processed == None).all()  # noqa: E711
    for n in n10ns:
        data = n.data
        data['server'] = SERVER
        data['url_prefix'] = PREFIX
        tmpl = j2env.get_template('email_{}.html'.format(n.type))
        subject = subjects[n.type]
        msg = tmpl.render(**data)
        send_html_email(subject, msg, data['email'])
        print('Processed:' + str(n))
        n.processed = func.now()
        session.commit()


def main():
    if __name__ == '__main__':
        notifications()


main()
