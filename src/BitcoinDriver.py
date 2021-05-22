import time

from .Parser import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class BitcoinParser(Parser):
    type = 'bitcoin'

    def __init__(self):
        # super().__init__()
        self._fill_requests()

    def _roll(self, index=None):
        if index:
            self.driver.get(self._build_url(index))
        else:
            self.driver.get(self._build_url('random'))

    def _parse_element(self, element):
        element_classes = element.get_attribute('class').split(" ")
        wallet_type = ""
        if self.wallet_types[1] in element_classes:
            wallet_type = self.wallet_types[1]
        elif self.wallet_types[3] in element_classes:
            wallet_type = self.wallet_types[3]
        
        element_raw_data = repr(element.text).replace("'", "").split('\\')

        balance = element_raw_data[0].split(' ')[0] + ' ' + element_raw_data[0].split(' ')[1]
        
        key = element_raw_data[1]
        
        return wallet_type, balance, key

    def run(self):
        self.driver = webdriver.Chrome()

        self._roll()
        #pass captcha once
        self._pass_captcha()

        while True:
            self._load_page()
            print("loaded page")
            self._check_wallets()
            time.sleep(1)
            self._roll()

    def test_run(self):
        i = 1
        self.driver = webdriver.Chrome()

        self._roll(index=i)
        #pass captcha once
        #self._pass_captcha()

        while True:
            i += 1
            self._load_page()
            print("loaded page")
            self._check_wallets()
            time.sleep(5)
            self._roll(index=i)
