# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 19:20:17 2020

@author: Ubaldo Peralta Sánchez
"""

class Analysis():

    def __init__(self, driver):
        self.driver = driver

    def getPayout(self):
        """ Getting the payout to determine the bet. No params"""
        payout = self.driver.find_element_by_xpath(
            '//*[@class="action-high-low button-call-wrap"]'
            '/a/span/span/span/span').text
        return float(payout[1:-1])/100

    def getTrend(self):
        """ Returning the trend. The trend refers to the percent
        of people that is going higher and lower. No params"""
        trend = self.driver.find_element_by_xpath(
            '//*[@class="progress-wrapper"]'
            '//div[last()]/i').text  # higher trend
        print(f"the trend is {trend}")
        return float(trend[:-1])
