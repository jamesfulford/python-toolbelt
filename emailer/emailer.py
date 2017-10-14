# email.py
# python 2.5
# by James Fulford
# uses gmail to send emails
# last edited on 8/8/2016

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Email:
    def __init__(self, sender, password):
        self.sender = sender
        self.message = MIMEMultipart()
        self.message['From'] = sender
        self.message['Reply-to'] = sender
        self.password = password

    def craft_new(self, subject, message):
        self.message['Subject'] = subject
        self.message.attach(MIMEText(message))

    def attach_file(self, path):
        """
        Path must lead to file to attach.
        """
        phile = open(path, 'rb')
        attachment = MIMEApplication(phile.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=phile.name)
        self.message.attach(attachment)

    def picture(self, path):
        phile = open(path, 'rb')
        image = MIMEImage(phile.read(), name=phile.name)
        self.message.attach(image)

    def send(self, to):
        """
        Sends email directly to one person
        """
        self.message['To'] = to
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(self.message['From'], self.password)
        server.sendmail(self.message['From'], [to], self.message.as_string())

    def mass_send(self, receivers):
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login(self.message['From'], self.password)
        server.sendmail(self.message['From'], receivers, self.message.as_string())
