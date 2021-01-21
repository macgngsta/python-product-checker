import os

import requests

class MailgunNotifier:
    @staticmethod
    def send_email(subject, message):

        mailgun_url =os.getenv('MAILGUN_BASE_URL')
        mailgun_apikey = os.getenv('MAILGUN_APIKEY')
        mailgun_from = os.getenv('MAILGUN_FROM')
        mailgun_to = os.getenv('MAILGUN_TO')

        to_array = []
        if ',' in mailgun_to:
            for to_recip in mailgun_to.split():
                quoted = '"'+to_recip+'"'
                to_array.append(quoted)
        else:
            quoted = '"' + mailgun_to + '"'
            to_array.append(quoted)

        return requests.post(mailgun_url, auth=("api",mailgun_apikey), data={
            "from": mailgun_from,
            "to":[','.join(to_array)],
            "subject": subject,
            "text":message
        })
