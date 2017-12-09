#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simulated account that can be used to test out strategies
without risk of losing any real money
"""
import datetime
import krakenex

from .Authenticator import Authenticator
from .PriceSample import PriceSample


class PracticeAuthenticator(Authenticator):
    """
    A simulated account that can be used to test out strategies
    without risk of losing any real money
    """

    def __init__(self, starting_balance, target_currency, account_currency):
        self._target_currency = target_currency
        self._target_balance = 0
        self._account_currency = account_currency
        self._account_balance = starting_balance
        self._api = krakenex.API()
        self.last_price = None

    def get_pair(self):
        return 'X' + self.target_currency() + 'Z' + self.price_currency()

    def target_currency(self):
        return self._target_currency

    def price_currency(self):
        return self._account_currency

    def get_current_price(self):

        # Query the public API
        response = self._api.query_public(
            'Depth', {'pair': self.get_pair(), 'count': '1'})

        # Check for errors
        if len(response['error']) is not 0:
            raise RuntimeError(str(response['error']))

        # Build a `PriceSample` to return
        cost = response['result'][self.get_pair()]['asks'][0][0]
        date = datetime.datetime.now()
        price = PriceSample(
            cost, date, self.target_currency(), self.price_currency())

        self.last_price = price
        return price

    def get_account_balance(self):
        return self._account_balance

    def get_holdings(self):
        return self._target_balance

    def buy(self, n_shares):
        super().buy(n_shares)

        if self.last_price is None:
            self.get_current_price()

        cost = self.last_price.price * n_shares
        if cost > self.get_account_balance():
            raise ValueError('Note enough funds')

        self._account_balance -= cost
        self._target_balance += n_shares

    def sell(self, n_shares):
        super().sell(n_shares)

        if self.last_price is None:
            self.get_current_price()

        profit = self.last_price.price * n_shares
        if n_shares > self.get_holdings():
            raise ValueError('You do not have that many shares')

        self._target_balance -= n_shares
        self._account_balance += profit
