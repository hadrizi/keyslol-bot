import requests

from selenium.common.exceptions import NoSuchElementException

from urllib.parse import urlunsplit, urlencode
from string import Template

class Parser:
    driver = None

    type = None

    url_scheme = "https"
    netloc = "keys.lol"

    requests = {
        'base': ['GET', '/$type'],
        'random': ['GET', '/$type/random'],
    }

    wallet_types = [
        'loading', # grey color, wallet is being checked
        'used',    # yellow color, wallet was used by someone
        'empty',   # red color, wallet is empty
        'filled'   # green color, THIS IS WHAT WE ARE LOOKING FOR
    ]

    def run(self):
        pass

    def test_run(self):
        pass

    def _roll(self, index=None):
        pass
        
    def _parse_element(self, element):
        pass

    def _build_url(self, req_op):
        # params = urlencode(self.url_params)
        if req_op not in self.requests.keys():
            return urlunsplit((self.url_scheme, self.netloc, self.requests['base'][1]+f"/{req_op}", None, ""))
        else:
            return urlunsplit((self.url_scheme, self.netloc, self.requests[req_op][1], None, ""))

    def _fill_requests(self):
        for request in self.requests.keys():
            t = Template(self.requests[request][1])
            self.requests[request][1] = t.substitute(type=self.type)

    def _load_page(self):
        while True:
            try:
                self.driver.find_element_by_xpath(f"//div[@data-loaded='0']")
            except NoSuchElementException:
                break

    def _check_wallets(self):
        try:
            elements = self.driver.find_elements_by_xpath(f"//div[contains(@class, '{self.wallet_types[1]}') or contains(@class, '{self.wallet_types[3]}')]")
            for element in elements:
                wallet_type, balance, key = self._parse_element(element)
                print(f"{wallet_type} {balance} {key}")
        except NoSuchElementException:
            pass

    def _pass_captcha(self):
        input("Press ENTER after filling CAPTCHA")
        self.driver.find_element_by_xpath("//form/button[@class='btn mt-8']").click()
