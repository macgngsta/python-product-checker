# -------------------------------
# STRATEGY:
# login, get token, check for slots available
# -------------------------------
import random
import sched
import time

from checker.common.mailgun_notifier import MailgunNotifier
from checker.common.setup_logger import logger
from checker.common.twilio_notifier import TwilioNotifier


class Checker:

    def __init__(self):
        self.strategies = []
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.reports = []

    ##-------------------------------

    def execute(self):
        counter = 1
        self.run_tasks()
        self.send_report()
        self.scheduler.run()

    ##-------------------------------

    def run_tasks(self):
        #random interval between 5 min and 7 minutes
        interval = random.randint(300, 420)
        # seconds delay 300
        # schedule the next one?
        e1 = self.scheduler.enter(interval, 1, self.run_tasks)

        logger.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} running...")
        for strategy in self.strategies:
            report = strategy.execute()
            self.reports.append(report)

    ##-------------------------------

    def send_report(self):

        #every 1 hr, send a report
        e2 = self.scheduler.enter(3600, 1, self.send_report)

        logger.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} sending report...")

        msg=''
        is_first = True
        for rep in self.reports:
            if is_first:
                is_first=False
            else:
                msg+=' /r/n '
            msg+=rep.to_string()

        MailgunNotifier.send_email('Vaccine Slot Check Results', msg)

        #clear the reports
        self.reports = []

    ##-------------------------------

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

# -------------------------------


