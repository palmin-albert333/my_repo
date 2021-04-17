import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendMail:
    smtp_host = ''
    smtp_port = ''
    smtp_user = ''
    smtp_password = ''

    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send(self, to, subject, body):
        message = MIMEMultipart()
        message['From'] = self.smtp_user
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            session = smtplib.SMTP(self.smtp_host, self.smtp_port)
            session.starttls()
            session.login(self.smtp_user, self.smtp_password)
            session.sendmail(self.smtp_user, to, message.as_string())
            session.quit()
        except smtplib.SMTPAuthenticationError as e:
            print('Error[%s]: %s' % (e.smtp_code, e.smtp_error.decode('utf-8')))

