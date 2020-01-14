# BSD 3-Clause License
#
# Copyright (c) 2018, Pruthvi Kumar All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities

__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "BSD 3-Clause License"
__version__ = "1.0"


class ProtonEmail(object):
    """
    PROTONs email client.
    """
    email_logger = LogUtilities().get_logger(log_file_name='emailer_logs',
                                             log_file_path='{}/trace/emailer_logs.log'.format(ProtonConfig.ROOT_DIR))
    __sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

    def __init__(self):
        super(ProtonEmail, self).__init__()

    @staticmethod
    def __email_decorator(html_content):
        """
        Decorates email with disclaimer, logo and other good formatting.
        :param html_content: The content that user desires
        :return: Formatted HTML content.
        """
        dont_reply_warning_text = '<strong>PS: Please do not reply to this email. This email may not be monitored. ' \
                                  'For any queries, please contact support ' \
                                  'for {} at {}.</strong>'.format(os.environ.get('APP_NAME'),
                                                                  os.environ.get('APP_SUPPORT_EMAIL'))

        proton_promotion_text = '<span style="font-size:8pt; font-family:Arial, sans-serif; color:#6a737d;"> ' \
                                'This email & the underlying software for {} is powered by the ' \
                                '<a href="https://github.com/PruthviKumarBK/PROTON">PROTON framework</a> - ' \
                                'Ⓒ <a href="https://adroitcorp.com.au">Adroit Software Corporation</a>' \
                                '</span>'.format(os.environ.get('APP_NAME'))

        disclaimer_text = '<span style="font-size:8pt; font-family:Arial, sans-serif; color:#9b9b9b;"> ' \
                          'The content of this email is confidential and intended for the recipient specified in ' \
                          'message only. It is strictly forbidden to share any part of this message with any ' \
                          'third party, without a written consent of the sender. If you received this message by ' \
                          'mistake, please forward to {} and follow with its deletion, ' \
                          'so that we can ensure such a mistake does not occur in the future.' \
                          '</span>'.format(os.environ.get('APP_SUPPORT_EMAIL'))

        formatted_content = '{}' \
                            '<br />' \
                            '<hr />' \
                            '{}' \
                            '<br />' \
                            '<br />' \
                            '{}' \
                            '<br />' \
                            '<br />' \
                            '{}'.format(html_content, dont_reply_warning_text, disclaimer_text, proton_promotion_text)

        return formatted_content

    @classmethod
    def send_email(cls, to_email, subject, html_content, from_email='proton_framework@apricity.co.in'):
        """
        PROTONs postman.

        :param to_email: valid email to which email needs to be sent to.
        :param subject: Email subject
        :param html_content: Email content.(Can include HTML markups)
        :param from_email: valid email from which email has to be sent from. (default: proton_framework@apricity.co.in)
        :return: A dictionary containing email status code, email body and email headers.
        """
        try:

            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=ProtonEmail.__email_decorator(html_content))
            response = cls.__sg.send(message)
            return {
                'email_status_code': response.status_code,
                'email_body': response.body,
                'email_headers': response.headers
            }

        except Exception as e:
            cls.email_logger.exception('[Email]: Unable to send email. Details to follow.')
            cls.email_logger.exception(str(e))




