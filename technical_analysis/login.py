# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:47:34 2020

@author: uba_p
"""
from time import sleep
import os

class GoogleLogin():
    
    def __init__(self, driver):
        
        self.driver = driver
        """ Sing in pocketoption with google. No params"""
        sleep(2)
        google_sign_in = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/div/div"
            "/div[3]/form/div[5]/div[1]/a[2]")
        google_sign_in.click()
        sleep(3)
        email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email.send_keys(os.environ['USER'])
        sleep(3)
        next = self.driver.find_element_by_xpath('//* [@id="identifierNext"]')
        next.click()
        sleep(3)
        pwd = self.driver.find_element_by_xpath(
            '//*[@id="password"]/div[1]/div/div[1]/input')
        pwd.send_keys(os.environ['LETSGO'])
        sleep(3)
        next = self.driver.find_element_by_xpath('//*[@id="passwordNext"]')
        next.click()
        sleep(15)