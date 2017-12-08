#!/usr/bin/env python 
# -*- coding: utf-8 -*-

class Trader:

    def __init__(self, authenticator, algorithm):
        self.authenticator = authenticator
        self.algorithm = algorithm

    def begin_trading():

        for loop:
            self.authenticator.get_current_price()


        if len(data) > self.algorithm.min_samples:
            buy = self.algorithm.make_decision(data)
            if buy:
                self.authenticator.buy(1)


trader = Trader(CoinCheckAuthenticator(), NagatomoAlgorithm())
trader.start_trading()