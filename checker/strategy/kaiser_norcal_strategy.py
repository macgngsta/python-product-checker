import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import requests
from selenium.webdriver.support.wait import WebDriverWait
import os

from checker.common.report_object import ReportObject
from checker.common.setup_logger import logger
from checker.common.session_object import SessionObject
from checker.common.twilio_notifier import TwilioNotifier

from dotenv import load_dotenv
load_dotenv()

class KaiserNorCal:

    LOGIN_REQUEST = 'https://mydoctor.kaiserpermanente.org/ncal/appointments/#/selectFacility/covid19-vaccination/dose1-evisit'
    FACILITIES_REQUEST = 'https://mydoctor.kaiserpermanente.org/mdo/api/v2/appointments/covid_dose1_evisit/facilities'
    SLOT_REQUEST = 'https://mydoctor.kaiserpermanente.org/mdo/api/v2/appointments/covid_dose1_evisit/facilities'
    SLOT_DELETE = 'https://mydoctor.kaiserpermanente.org/mdo/api/v2/appointments/slot-locks'

    def __init__(self):
        self.name = "Kaiser Northern California"
        self.session = SessionObject()
        self.facilities = []

    ##-------------------------------
    ## EXECUTE
    ##-------------------------------

    def execute(self):
        start = time.perf_counter()

        report = ReportObject()
        report.strategy = self.name

        #build the session here
        if not self.session.is_active():
            logger.info('building session...')
            if self.do_login():
                facilities_json = self.get_facilities()

        #start processing - at this point we hopefully have a valid session
        logger.info('active session, making requests...')
        for facility in self.facilities:
            status = self.check_slots_by_facility(facility)
            if status ==1:
                TwilioNotifier.send_notification(f"found vaccine slot at {facility}")

            report.add_facility(facility, status)

        #build session
        #run code
        #if


        end = time.perf_counter()

        report.duration=end-start
        logger.info(report.to_string())

        return report

    ##-------------------------------

    def check_slots_by_facility(self, facility_code):
        logger.debug('checking for slots in facility '+ facility_code)
        #hit facility
        status = self.request_slots(facility_code)
        #delete the appointment
        self.delete_appointment()

        return status

    ##-------------------------------
    ## HELPER METHODS
    ##-------------------------------

    def do_login(self):
        login_u = os.getenv('KAISER_LOGIN')
        login_p = os.getenv('KAISER_PASSWORD')
        browser_path = os.getenv('PATH_TO_FIREFOX_DRIVER')

        #set the time when i rebuild this
        self.created_at=time.time()
        self.session.login = login_u

        opts = Options()
        opts.headless = True
        browser = Firefox(options=opts, executable_path=browser_path)
        browser.get(self.LOGIN_REQUEST)

        login_username_field = browser.find_element_by_id('username')
        login_username_field.send_keys(login_u)
        login_password_field = browser.find_element_by_id('password')
        login_password_field.send_keys(login_p)

        login_submit = browser.find_element_by_id('sign-on')
        login_submit.submit()

        # need the browser to load the my doctor online page
        delay = 5
        try:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'member-select-id')))
            logger.debug('Page loaded.')
        except TimeoutException:
            logger.warning('Loading took too long...')
            return False

        cookie_list = []
        for cookie in browser.get_cookies():
            cookie_list.append(f"{cookie['name']}={cookie['value']}")
        cookie_str = '; '.join(cookie_list)

        self.session.cookies = cookie_str
        logger.debug(f"COOKIE: {cookie_str}")

        browser.close()

        #TODO: need to create a condition where the login doesnt work

        return True

    ##-------------------------------

    def get_facilities(self):
        logger.debug('getting facility list and token...')

        headers = {'Cookie': self.session.cookies}

        try:
            response = requests.get(self.FACILITIES_REQUEST, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logger.error("Oops: Something Else", err)
        else:
            if (response):
                t = response.json()

                if 'token' in t:
                    token = t['token']
                    logger.debug(f"TOKEN: {token}")
                    self.session.token = token
                    self.is_good = True

                return t
            else:
                logger.warning('Response for facilities was empty')

        return None


    ##-------------------------------

    def request_slots(self, facility):
        logger.debug('requesting slots for '+ facility)

        params = {}
        params['tokenIdQuery'] = self.session.token
        params['showFirstAvailable'] = 'true'
        params['startDate'] = '01%2F20%2F2021'
        params['bookingGuideline'] = 'COVIDVACCINE'

        uri = f"{self.SLOT_REQUEST}/{facility}/slot-locks"
        headers = {'Cookie': self.session.cookies, 'Content-Type': 'application/json'}

        try:
            response = requests.post(uri, headers=headers, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logger.error("Oops: Something Else", err)
        else:
            if (response):
                t = response.json()
                if not t['slots']:
                    logger.info(f"No slots available at: {facility}")
                    return 0
                else:
                    logger.info(f"SLOTS AVAILABLE: {facility}")
                    return 1

        logger.warning(f"Response for slots at {facility} was empty")
        return -1

    ##-------------------------------

    def delete_appointment(self):
        logger.debug('cleaning up appointments related to token...')

        headers = {'Cookie': self.session.cookies}

        params = {}
        params['tokenIdQuery'] = self.session.token

        try:
            response = requests.delete(self.SLOT_DELETE, headers=headers, params=params)
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logger.error("Oops: Something Else", err)