# -*- coding: utf-8 -*-
"""
@author: Ubaldo Peralta Sánchez
"""

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from math import ceil
from technical_analysis.login import GoogleLogin
from technical_analysis.analysis import Analysis

class Bot():

    _bets = []
    earned = 0

    url = "https://pocketoption.com/en/login"

    def __init__(self):
        """ Constructor of Bot"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        sleep(5)
        self.driver.get(self.url)

    def selectAsset(self):
        """ Select the Asset. Thinking What i want to do (still developing)"""
        sleep(2)
        closed = self.driver.find_element_by_xpath(
            '//*[@id="bar-chart"]/div/div/div[2]/div/div[1]/div[2]/ul/li[2]/a')
        closed.click()

    def Opentab(self):
        """ Opening tab. Thinking What i want to do"""
        sleep(2)
        Open = self.driver.find_element_by_xpath(
            '//*[@id="bar-chart"]/div/div/div[2]/div/div[1]/div[2]/ul/li[1]/a')
        Open.click()

    def buyHigherButton(self):
        """ Calling the bet higher (green button). No params"""
        print("Calling the bet higher")
        buy = self.driver.find_element_by_xpath(
            '//*[@class="action-high-low button-call-wrap"]/a')
        buy.click()

    def buyLowerButton(self):
        """ Calling the bet lower"""
        print("Calling the bet lower")
        buy = self.driver.find_element_by_xpath(
            '//*[@class="action-high-low button-put-wrap"]/a')
        buy.click()

    def setBet(self):
        """ Setting the bet using the payout reference. No params"""
        print("Setting the bet")
        price = self.driver.find_element_by_xpath(
            '//*[@class="block block--bet-amount"]/div[2]/div/div/div/input')
        price.clear()
        price.send_keys(Keys.BACK_SPACE)
        payout = Analysis(self.driver).getPayout()

        if len(self._bets) < 1:
            final_bet = ceil((1/payout) * 100) / 100.0
            self._bets.append(final_bet)
            price.send_keys(str(final_bet))
        else:
            final_bet = round(ceil((sum(self._bets)/payout) * 100) / 100.0)
            self._bets.append(final_bet)
            price.send_keys(str(final_bet))
        print(final_bet)

    def resetBet(self):
        """ clearing list of bets. No params"""
        self._bets.clear()

    def isActiveTrade(self):
        """ seeking for trades. If there are
        any live tradesm return True. No params."""
        trade = 0
        try:
            trade = self.driver.find_element_by_xpath(
                '//*[@id="bar-chart"]/div/div'
                '/div[2]/div/div[2]/div/div[3]/div[2]')
        except:
            trade = 0
            if(trade == 0):
                print("NO active trading")
                return False
        else:
            print("YES active trading")
            return True

    def getLastProfitBet(self):
        """ Returning the last bet. It is used to know if the next bet
        will be raising or if we have to restart the martingale. No params."""
        self.driver.find_element_by_xpath(
            '//*[@class="widget-slot__header"]'
            '/div[2]/ul/li[2]/a').click()  # Opening trade history
        sleep(5)
        last_bet = self.driver.find_element_by_xpath(
            "//div[@class='scrollbar-container deals-list ps']"
            "//div[5]/div[2]/div[2]").text
        self.driver.find_element_by_xpath(
            '//*[@class="widget-slot__header"]/div[2]/ul/li[1]/a').click()
        print(f"The last bet cash back were {last_bet}")
        return float(last_bet[1:])

    def run(self):
        """ launching app method. No params"""
        GoogleLogin(self.driver)  # login with google
        sleep(10)
        # At the moment giving 7 concatenated loosing bets
        while len(self._bets) < 8:
            if not self.isActiveTrade():  # If doesn't exist any trade
                if self.getLastProfitBet() < 1:  # If last bet were lost
                    #  depending on the trend. opening higher or lower
                    trend = Analysis(self.driver).getTrend()
                    if trend >= 90:
                        self.setBet()  # setting bet values
                        self.buyHigherButton()  # going higher
                        print("Higher bet")
                    elif trend <= 10:
                        self.setBet()  # setting bet values
                        self.buyLowerButton()  # going lower
                        print("Lower bet")
                else:  # If last bet were lost
                    print("Lost bets " + str(sum(self._bets)))

                    self.earned += 1  # Every win bet we earn a dollar
                    print(f"earned {self.earned}")
                    self.resetBet()
                    trend = Analysis(self.driver).getTrend()
                    if trend >= 90:
                        self.setBet()  # setting bet values
                        self.buyHigherButton()  # going lower
                        print("Higher bet")
                    elif trend <= 10:
                        self.setBet()  # setting bet values
                        self.buyLowerButton()  # going lower
                        print("Lower bet")
            sleep(10)
