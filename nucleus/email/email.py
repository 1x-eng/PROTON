import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class ProtonEmail(object):

    def __init__(self):
        super(ProtonEmail, self).__init__()
        self.message = Mail(
            from_email='from_email@example.com',
            to_emails='pruthvikumar.123@gmail.com',
            subject='Sending with Twilio SendGrid is Fun',
            html_content='<strong>and easy to do anywhere, even with Python</strong>')

        self.sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


