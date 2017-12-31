#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains unit tests to ensure that `Trader` makes the proper calls to
its members and that its state is correct following each trade cycle.
"""
from unittest import TestCase
from baibaitrader.Trader import Trader
from .mocks import MockAlgorithm, MockAuthenticator


class TestTrader(TestCase):

    def setUp(self):
        self.trader = Trader('unit_tests',
                             MockAuthenticator(),
                             MockAlgorithm(),
                             update_interval=42,
                             output_console=False)

    def test_is_running_starts_false(self):
        assert self.trader.is_running is False

    def test_update_interval_gets_set(self):
        assert self.trader.update_interval == 42

    def test_thread_starts_and_stops(self):
        self.trader.begin_trading()
        assert self.trader.is_running is True
        self.trader.stop_trading()
        assert self.trader.is_running is False

    def test_cyle_checks_price_exactly_once(self):
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_checks == 1

    def test_cycle_fetches_data_exactly_once(self):
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_data == 1

    def test_check_buy_exactly_once(self):
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_check_buy == 1

    def test_not_check_sell_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_check_sell == 0

    def test_check_both_once_when_not_buy(self):
        self.trader.algorithm.should_buy = False
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_check_buy == 1
        assert self.trader.algorithm.n_check_sell == 1

    def test_doesnt_check_sell_volume_when_no_sell(self):
        self.trader.algorithm.should_sell = False
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_sell_volume == 0

    def test_doesnt_check_buy_volume_when_no_buy(self):
        self.trader.algorithm.should_buy = False
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_buy_volume == 0

    def test_check_buy_volume_once_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_buy_volume == 1

    def test_sell_volume_once_when_sell(self):
        self.trader.algorithm.should_sell = True
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_sell_volume == 1

    def test_does_not_buy_when_no_buy(self):
        self.trader.algorithm.should_buy = False
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_buys == 0

    def test_does_not_sell_when_no_sell(self):
        self.trader.algorithm.should_sell = False
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_sells == 0

    def test_does_buy_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.algorithm.n_buy_volume == 1

    def test_does_sell_when_sell(self):
        self.trader.algorithm.should_sell = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_sells == 1

    def test_checks_balance_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_balance == 1

    def test_not_check_balance_when_no_buy(self):
        self.trader.algorithm.should_buy = False
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_balance == 0

    def test_checks_holdings_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_holdings == 1
    
    def test_check_holdings_when_sell(self):
        self.trader.algorithm.should_sell = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_holdings == 1

    def test_not_check_holdings_when_no_buy_or_sell(self):
        self.trader.algorithm.should_buy = False
        self.trader.algorithm.should_sell = False
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_holdings == 0

    def test_buys_once_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_buys == 1

    def test_sells_once_when_sell(self):
        self.trader.algorithm.should_sell = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_sells == 1

    def test_no_sell_when_buy(self):
        self.trader.algorithm.should_buy = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_sells == 0

    def test_no_buy_when_sell(self):
        self.trader.algorithm.should_sell = True
        self.trader.perform_one_cycle()
        assert self.trader.authenticator.n_buys == 0
