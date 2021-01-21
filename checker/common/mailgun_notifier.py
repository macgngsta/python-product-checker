import os
import requests

from checker.common.setup_logger import logger

class MailgunNotifier:
    @staticmethod
    def send_email(subject, message):

        mailgun_url =os.getenv('MAILGUN_BASE_URL')
        mailgun_apikey = os.getenv('MAILGUN_APIKEY')
        mailgun_from = os.getenv('MAILGUN_FROM')
        mailgun_to = os.getenv('MAILGUN_TO')

        to_array = []
        if ',' in mailgun_to:
            to_array = mailgun_to.split(',')
        else:
            to_array.append(mailgun_to)

        return requests.post(mailgun_url+"/messages", auth=("api",mailgun_apikey), data={
            "from": mailgun_from,
            "to":to_array,
            "subject": subject,
            "text":message
        })