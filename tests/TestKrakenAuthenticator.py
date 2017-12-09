#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from nose.tools import raises

from bitbaibai.KrakenAuthenticator import KrakenAuthenticator
from bitbaibai.PriceSample import PriceSample

from .mocks import MockKrakenAPI

class TestKrakenAuthenticator(TestCase):

    def setUp(self):
        self.auth = KrakenAuthenticator('tests/fake_key.key', 'XBT', 'USD')
        self.auth._api = MockKrakenAPI()

    def test_pair(self):
        assert self.auth.get_pair() == 'XXBTZUSD'
    
    def test_price_currency(self):
        assert self.auth.price_currency() == 'USD'

    def test_target_currency(self):
        assert self.auth.target_currency() == 'XBT'

    def test_returns_price(self):
        self.auth._api.should_fail = False
        x = self.auth.get_current_price()
        assert type(x) is PriceSample

    @raises(RuntimeError)
    def test_get_current_price_fails(self):
        self.auth._api.should_fail = True
        self.auth.get_current_price()

    def test_current_price_queries_once(self):
        self.auth.get_current_price()
        assert self.auth._api.n_query_pub == 1

    def test_check_balance_success(self):
        x = self.auth.get_account_balance()
        assert x == 99.9

    @raises(RuntimeError)
    def test_check_balance_fails(self):
        self.auth._api.should_fail = True
        self.auth.get_account_balance()

    def test_check_balance_calls_api_once(self):
        self.auth.get_account_balance()
        assert self.auth._api.n_query_account == 1

    def test_check_holdings_success(self):
        x = self.auth.get_holdings()
        assert x == 99.9

    @raises
    def test_check_holdings_fails(self):
        self.auth._api.should_fail = True
        self.auth.get_holdings()

    def test_check_holdings_calls_api_once(self):
        self.auth._api.get_holdings()
        assert self.auth._api.n_query_holdings == 1

