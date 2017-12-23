#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains unit tests to ensure that `AlgorithmTester` is working
correclty
"""
import numpy as np
from datetime import datetime, timedelta
from unittest import TestCase
from bitbaibai import AlgorithmTester, PriceSample, TransationRecord
from bitbaibai.utils import read_price_history
from .mocks import MockAlgorithm

log_file = 'tests/test_log.log'


class TestAlgorithmTester(TestCase):

    def setUp(self):
        self.tester = AlgorithmTester(log_file, MockAlgorithm(), 5.0, 311.0)

    def sample_data(self):
        n = 1000
        sigma = 10
        mu = 500
        values = np.random.normal(mu, sigma, n)
        values[values >= 3 * sigma + mu] = mu
        dt = timedelta(minutes=10)
        data = []
        for i in range(n):
            price = values[i]
            date = datetime.now() - dt * i
            sample = PriceSample(price, date, 'XBT', 'USD')
            data.append(sample)

        def replace_price(n, new_price):
            old = data[n]
            new = PriceSample(new_price, old.date,
                              old.currency, old.price_currency)
            data[n] = new

        replace_price(248, 998)
        replace_price(249, 999)
        replace_price(250, 1000)
        replace_price(251, 999)
        replace_price(252, 998)

        replace_price(748, 102)
        replace_price(749, 101)
        replace_price(750, 100)
        replace_price(751, 101)
        replace_price(752, 102)
        return data

    def test_initializer_sets_logfile(self):
        assert self.tester.logfile == log_file

    def test_initializer_sets_algorithm(self):
        assert isinstance(self.tester.algorithm, MockAlgorithm)

    def test_initializer_sets_holdings(self):
        assert self.tester.holdings == 5.0

    def test_initializer_sets_balance(self):
        assert self.tester.balance == 311.0

    def test_starts_no_buys_sells(self):
        assert self.tester.buys == []
        assert self.tester.sells == []

    def test_history_starts_empty(self):
        assert self.tester.holdings_history == []
        assert self.tester.balance_history == []

    def test_simulating_calls_process_data_once_per_log_line(self):
        num_prices = len(read_price_history(log_file))
        self.tester.simulate_trading(draw=False)
        assert self.tester.algorithm.n_data == num_prices

    def test_checks_should_buy(self):
        num_prices = len(read_price_history(log_file))
        self.tester.simulate_trading(draw=False)
        assert self.tester.algorithm.n_check_buy == num_prices

    def test_checks_should_sell(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_buy = False
        self.tester.simulate_trading(draw=False)
        assert self.tester.algorithm.n_check_sell == num_prices

    def test_checks_buy_volume(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_buy = True
        self.tester.simulate_trading(draw=False)
        assert self.tester.algorithm.n_buy_volume == num_prices

    def test_checks_sell_volume(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_sell = True
        self.tester.simulate_trading(draw=False)
        assert self.tester.algorithm.n_sell_volume == num_prices

    def test_add_transaction_for_buy(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_buy = True
        self.tester.simulate_trading(draw=False)
        assert len(self.tester.buys) == num_prices

    def test_adds_transaction_for_sell(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_sell = True
        self.tester.simulate_trading(draw=False)
        assert len(self.tester.sells) == num_prices

    def test_buy_updates_holdings_history(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_buy = True
        self.tester.simulate_trading(draw=False)
        assert len(self.tester.holdings_history) == num_prices + 1

    def test_buy_updates_balance_history(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_buy = True
        self.tester.simulate_trading(draw=False)
        assert len(self.tester.balance_history) == num_prices + 1

    def test_sell_updates_holdings_history(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_sell = True
        self.tester.simulate_trading(draw=False)
        assert len(self.tester.holdings_history) == num_prices + 1

    def test_sell_updates_balance_history(self):
        num_prices = len(read_price_history(log_file))
        self.tester.algorithm.should_sell = True
        self.tester.simulate_trading(draw=False)
        assert len(self.tester.balance_history) == num_prices + 1

    def test_buy_updates_balance(self):
        original_balance = self.tester.balance
        self.tester.algorithm.should_buy = True
        self.tester.simulate_trading(draw=False)
        assert self.tester.balance != original_balance

    def test_buy_updates_holdings(self):
        original_holdings = self.tester.holdings
        self.tester.algorithm.should_buy = True
        self.tester.simulate_trading(draw=False)
        assert self.tester.holdings != original_holdings

    def test_sell_updates_balance(self):
        original_balance = self.tester.balance
        self.tester.algorithm.should_sell = True
        self.tester.simulate_trading(draw=False)
        assert self.tester.balance != original_balance

    def test_sell_updates_holdings(self):
        original_holdings = self.tester.holdings
        self.tester.algorithm.should_sell = True
        self.tester.simulate_trading(draw=False)
        assert self.tester.holdings != original_holdings

    def test_plot(self):
        data = self.sample_data()
        prices = [d.price for d in data]
        min_idx = np.argmin(prices)
        max_idx = np.argmax(prices)

        buy = TransationRecord(
            'buy', data[min_idx].date, 'XBT', data[min_idx].price,
            1, data[min_idx].price * 1, 'USD')
        sell = TransationRecord(
            'sell', data[max_idx].date, 'XBT', data[max_idx].price,
            1, data[max_idx].price * 1, 'USD')
        self.tester.sample_history = data
        self.tester.buys = [buy]
        self.tester.sells = [sell]
        self.tester.holdings_history = [
            (7, data[-1].date), (2, buy.date), (5, sell.date)]
        self.tester.balance_history = [
            (1000, data[-1].date), (5000, buy.date), (3000, sell.date)]
        # self.tester.plot_results()
