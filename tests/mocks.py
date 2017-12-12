#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file provides utilities for testing
"""
import datetime
from bitbaibai import Algorithm, Authenticator, PriceSample


class MockAlgorithm(Algorithm):
    n_data = 0
    n_check_buy = 0
    n_check_sell = 0
    n_buy_volume = 0
    n_sell_volume = 0
    should_buy = False
    should_sell = False

    def process_data(self, samples):
        self.n_data += len(samples)

    def check_should_buy(self):
        self.n_check_buy += 1
        return self.should_buy

    def check_should_sell(self):
        self.n_check_sell += 1
        return self.should_sell

    def determine_buy_volume(self, price, holdings, account_balance):
        self.n_buy_volume += 1
        return 50.0

    def determine_sell_volume(self, price, holdings, account_balance):
        self.n_sell_volume += 1
        return 25.0


class MockAuthenticator(Authenticator):
    n_checks = 0
    n_buys = 0
    n_sells = 0
    n_holdings = 0
    n_balance = 0
    should_fail = False

    def get_current_price(self):
        if not self.should_fail:
            self.n_checks += 1
            return PriceSample(42.0, datetime.datetime.now(),
                               self.target_currency(), self.price_currency())
        else:
            raise Exception('')

    def buy(self, n_shares):
        if not self.should_fail:
            self.n_buys += 1 
        else:
            raise Exception('')

    def sell(self, n_shares):
        if not self.should_fail:
            self.n_sells += 1
        else:
            raise Exception('')

    def price_currency(self):
        return "USD"

    def target_currency(self):
        return "BTC"

    def get_holdings(self):
        self.n_holdings += 1
        return 2.7

    def get_account_balance(self):
        self.n_balance += 1
        return 20000.0


class MockKrakenAPI:

    n_query_pub = 0
    n_query_private = 0

    should_fail = False

    def query_private(self, endpoint):
        self.n_query_private += 1
        if self.should_fail:
            return {'error': ['Bad News!']}
        else:
            return {'error': ['Bad News!']}

    def query_public(self, endpoint, json):
        self.n_query_pub += 1
        if self.should_fail:
            return {'error': ['Bad News!']}
        else:
            return {'error': [],
                    'result': {
                        'XXBTZUSD': {
                            'asks': [
                                [500]
                            ]
                        }
            }
            }
