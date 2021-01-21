from twilio.rest import Client

from checker.common.setup_logger import logger
import os

##-------------------------------

class TwilioNotifier:

    @staticmethod
    def send_notification(msg):
        logger.info('sending notification(s)')

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        sender = os.getenv('TWILIO_FROM')
        recip = os.getenv('TWILIO_TO')

        recipients = []

        if ',' in recip:
            recipients = recip.split(',')
        else:
            recipients.append(recip)

        twilio_client = Client(account_sid, auth_token)

        for rec in recipients:
            msg = twilio_client.messages.create(to=rec, from_=sender, body=msg)