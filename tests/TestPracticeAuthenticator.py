#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the PracticeAuthenticator to make sure it tracks balances properly
"""
from unittest import TestCase
from nose.tools import raises

from baibaitrader import PracticeAuthenticator
from baibaitrader import PriceSample

from .mocks import MockKrakenAPI


class TestPracticeAuthenticator(TestCase):

    def setUp(self):
        self.auth = PracticeAuthenticator(10000, 'XBT', 'USD')
        self.auth._api = MockKrakenAPI()

    def test_initial_target_balance(self):
        assert self.auth.get_holdings() == 0

    def test_initial_balance_converted_to_float(self):
        assert isinstance(self.auth.get_account_balance(), float)

    def test_initial_account_balance(self):
        assert self.auth.get_account_balance() == 10000.0

    def test_target_currency(self):
        assert self.auth.target_currency() == 'XBT'

    def test_account_currency(self):
        assert self.auth.price_currency() == 'USD'

    def test_pair(self):
        assert self.auth.get_pair() == 'XXBTZUSD'

    def test_current_price(self):
        x = self.auth.get_current_price()
        assert isinstance(x, PriceSample)

    def test_current_prices_queries_ones(self):
        self.auth.get_current_price()
        assert self.auth._api.n_query_pub == 1

    @raises(RuntimeError)
    def test_current_price_fails(self):
        self.auth._api.should_fail = True
        self.auth.get_current_price()

    def test_check_holdings(self):
        self.auth._target_balance = 10.1
        x = self.auth.get_holdings()
        assert x == 10.1

    def test_buy_success(self):
        self.auth._account_balance = 1000
        self.auth.buy(2)  # $500/share (see MockKrakenAPI)
        assert self.auth.get_account_balance() == 0

    @raises(ValueError)
    def test_cannot_buy(self):
        self.auth._account_balance = 500
        self.auth.buy(2)

    @raises(ValueError)
    def test_cannot_buy_zero(self):
        self.auth.buy(0)

    @raises(ValueError)
    def test_cannot_buy_negative(self):
        self.auth.buy(-2)

    def test_sell_succes(self):
        self.auth._account_balance = 0
        self.auth._target_balance = 2
        self.auth.sell(2)
        assert self.auth.get_account_balance() == 1000.0

    @raises(ValueError)
    def test_cannot_sell(self):
        self.auth._target_balance = 2
        self.auth.sell(3)

    @raises(ValueError)
    def test_cannot_sell_zero(self):
        self.auth.sell(0)

    @raises(ValueError)
    def test_cannot_sell_negative(self):
        self.auth.sell(-5)
