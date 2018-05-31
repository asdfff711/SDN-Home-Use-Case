# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("https://www.youtube.com/")
        driver.find_element_by_id("logo-icon-container").click()
        driver.find_element_by_name("search_query").click()
        driver.find_element_by_name("search_query").click()
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | name=search_query | ]]
        driver.find_element_by_name("search_query").click()
        driver.find_element_by_name("search_query").clear()
        driver.find_element_by_name("search_query").send_keys("cats")
        driver.find_element_by_id("search-form").submit()
        driver.find_element_by_xpath("//img[contains(@src,'https://i.ytimg.com/vi/hY7m5jjJ9mM/hqdefault.jpg?sqp=-oaymwEXCPYBEIoBSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLB7rpNhtGZ59KEeHOhplLNlhqAM1g')]").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

