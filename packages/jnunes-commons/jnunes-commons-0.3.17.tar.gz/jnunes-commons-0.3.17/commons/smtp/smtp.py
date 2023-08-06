import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from commons.smtp.objects import EmailHtml, SmtpConf


def send_html_email(mail_object: EmailHtml):
    config = SmtpConf()

    message = MIMEMultipart('alternative')
    message['Subject'] = mail_object.subject
    message['From'] = _get_sender_email(mail_object, config)
    message['To'] = mail_object.to

    message.attach(MIMEText(mail_object.text_message, 'text'))
    message.attach(MIMEText(mail_object.html_message, 'html'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.smtp, config.port, context=context) as server:
        server.login(config.user, config.password)
        server.sendmail(_get_sender_email(mail_object, config), mail_object.to, message.as_string())


def _get_sender_email(mail_object: EmailHtml, config: SmtpConf):
    if mail_object.sender_name_on_subject and mail_object.sender_name is not None:
        return f'{mail_object.sender_name} <{config.user}>'
    else:
        return f'{config.app_name} <{config.user}>'
