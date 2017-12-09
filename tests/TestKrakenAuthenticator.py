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

    def test_get_current_price_success(self):
        self.auth._api.should_fail = False
        x = self.auth.get_current_price()
        assert type(x) is PriceSample

    @raises(RuntimeError)
    def test_get_current_price_fails(self):
        self.auth._api.should_fail = True
        self.auth.get_current_price()
