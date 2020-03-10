from time import sleep

from mapianist import setup_chrome
from settings import GOOGLE_EMAIL, GOOGLE_PASSWORD


class ChromeDriver:
    driver = None

    def __init__(self):
        print('Initialize ChromeDriver Start...')
        self.driver = setup_chrome()
        self.driver = self.sign_in_google()
        print('Initialize ChromeDriver Complete...')

    def sign_in_google(self):
        self.driver.get('https://accounts.google.com/signin/v2/identifier?hl=ko&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
        sleep(1)
        self.driver.find_element_by_name('Email').send_keys(GOOGLE_EMAIL)
        self.driver.find_element_by_name('signIn').click()
        sleep(1)
        self.driver.find_element_by_name('Passwd').send_keys(GOOGLE_PASSWORD)
        self.driver.find_element_by_id('signIn').click()
        sleep(1)
#        self.driver.find_element_by_id('submit_approve_access').click()
#        sleep(1)
        return self.driver
