# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 19:20:17 2020

@author: Ubaldo Peralta Sánchez
"""

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

import re
import os
#import copy
#import analize
class PocketBot():
    _bets = [0]
    buy = 0
    sell = 0
    # bet = 1
    url = "https://pocketoption.com/en/login"
    
    def __init__(self):
        """ Constructor of PocketBot"""
        self.driver = webdriver.Chrome()
        sleep(5)
        self.driver.get(self.url)
        
         #Login
    def google_login(self):
        """ Sing in pocketoption with google"""
        sleep(2)
        google_sign_in =  self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div[3]/form/div[5]/div[1]/a[2]')
        google_sign_in.click()
        
        sleep(3)
        email = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email.send_keys(os.environ['USER'])
        sleep(3)
        next = self.driver.find_element_by_xpath('//* [@id="identifierNext"]')
        next.click()
        
        sleep(3)
        pwd = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        pwd.send_keys(os.environ['LETSGO'])
        sleep(3)
        next =self.driver.find_element_by_xpath('//*[@id="passwordNext"]')
        next.click()
        sleep(15)
        
    def selectAsset(self): 
        """ Select the Asset. Thinking What i want to do"""
        sleep(2)
        closed = self.driver.find_element_by_xpath('//*[@id="bar-chart"]/div/div/div[2]/div/div[1]/div[2]/ul/li[2]/a')
        closed.click()        
    
    def Opentab(self):
        """ Opening tab. Thinking What i want to do"""
        sleep(2)
        Open = self.driver.find_element_by_xpath('//*[@id="bar-chart"]/div/div/div[2]/div/div[1]/div[2]/ul/li[1]/a')
        Open.click()
        
    def buyHigherButton(self):
        """ Calling the bet higher"""
        buy = self.driver.find_element_by_xpath('//*[@class="action-high-low button-call-wrap"]/a') 
        buy.click()
        
    def buyLowerButton(self):
        """ Calling the bet lower"""
        buy = self.driver.find_element_by_xpath('//*[@class="action-high-low button-put-wrap"]/a')
        buy.click()

    def getPayout(self):
        """ Getting the payout to determine the bet"""
        payout = self.driver.find_element_by_xpath('//*[@class="action-high-low button-call-wrap"]/div/span').text
        return float(payout[2:])

    def getBetvalue(self):
        """"""
        value = self.driver.find_element_by_xpath('//*[@id="put-callbuttons-chart-1"]/div/div[3]/div[2]/div/div/div/input')
        valueAux = value.get_attribute('value')
        return int(re.search(r'\d+', valueAux).group())
        
        #GET IF PRICE OF LAST BET > 0
    def getDollars(self):
    
        lastBetMoney = self.driver.find_element_by_xpath('//*[@id="bar-chart"]/div/div/div[2]/div/div[2]/div/div[5]/div[2]/div[2]')
        lastBetMoneyAux = lastBetMoney.get_attribute("innerHTML")
        return int(re.search(r'\d+', lastBetMoneyAux).group())
        
    def getTrend(self):
        """The trend refers to the percent of people that is going higher. if trend > 50% people is buying, else people is going lower"""
        trend = self.driver.find_element_by_xpath('//*[@class="progress-wrapper"]/div/i').text  # higher trend
        return trend[:-1]
        
    def setBet(self):
        """ Setting the bet using the payout reference"""
        price = self.driver.find_element_by_xpath('//*[@class="block block--bet-amount"]/div[2]/div/div/div/input')
        
        if len(self._bets) < 1:
            final_bet = 1
            self._bets.append(final_bet)
        else:
            payout = self.getPayout()
            final_bet = sum(self._bets)/payout
            self._bets.append(final_bet)
            price.send_keys(final_bet)
        return price
    
    def isActiveTrade(self):
        trade = 0
        try:
            trade = self.driver.find_element_by_xpath('//*[@id="barchart"]/div/div/div[2]/div/div[2]/div/div[3]/div[2]')
        except:
            trade = 0
            if(trade == 0):
                return False
        else:
                return True
        
    
    def run(self):
        """ launching app method"""
        
        self.google_login()
        #self.buyHigherButton()
    
        self.setBet()
        """
        if int(self.getTrend()) >= 90:
            self.buyHigherButton()
        elif int(self.getTrend()) <= 10:
            self.buyLowerButton()
        """
bot = PocketBot()
bot.run()
print("Done")

