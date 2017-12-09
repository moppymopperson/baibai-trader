#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains unit tests to ensure that `Trader` makes the proper calls to
its members and that its state is correct following each trade cycle.
"""
from unittest import TestCase
from bitbaibai.Trader import Trader
from .mocks import MockAlgorithm, MockAuthenticator


class TestTrader(TestCase):

    def setUp(self):
        self.trader = Trader(MockAuthenticator(),
                             MockAlgorithm(),
                             update_interval=42)

    def test_is_running_starts_false(self):
        assert self.trader.is_running is False

    def test_update_interval_gets_set(self):
        assert self.trader.update_interval == 42

    def test_thread_starts_and_stops(self):
        self.trader.begin_trading()
        assert self.trader.is_running is True
        self.trader.stop_trading()
        assert self.trader.is_running is False

    def test_perform_cyle(self):
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_data == 1
        assert self.trader.authenticator.n_checks == 1

    def test_no_transaction(self):
        self.trader.algorithm.should_buy = False
        self.trader.algorithm.should_sell = False
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_check_buy == 1
        assert self.trader.algorithm.n_buy_volume == 0
        assert self.trader.algorithm.n_check_sell == 1
        assert self.trader.algorithm.n_sell_volume == 0
        assert self.trader.authenticator.n_buys == 0
        assert self.trader.authenticator.n_sells == 0

    def test_buy_transation(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_check_buy == 1
        assert self.trader.algorithm.n_buy_volume == 1
        assert self.trader.authenticator.n_sells == 0
        assert self.trader.authenticator.n_buys == \
            self.trader.algorithm.determine_buy_volume()

    def test_sell_transaction(self):
        self.trader.algorithm.should_sell = True
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_check_sell == 1
        assert self.trader.algorithm.n_sell_volume == 1
        assert self.trader.authenticator.n_buys == 0
        assert self.trader.authenticator.n_sells == \
            self.trader.algorithm.determine_sell_volume()
