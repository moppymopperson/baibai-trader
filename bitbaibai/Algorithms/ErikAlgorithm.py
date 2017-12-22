#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains an `Algorithm` developed by Erik Hornberger for automatically
determing when to buy and sell virtual currencies.
"""
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from .Algorithm import Algorithm
from ..TransationRecord import TransationRecord


class ErikAlgorithm(Algorithm):

    def __init__(self, sigma):
        self.sigma = sigma
        self.comparison_window = timedelta(days=2)
        self.data = []
        self.last_buy = None
        self.last_sell = None

    # Algorithm interface methods

    def process_data(self, price_samples):
        super().process_data(price_samples)
        price_samples.sort(key=lambda x: x.date)
        for sample in price_samples:
            self.data.insert(0, sample)

    def check_should_buy(self):
        super().check_should_buy()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_buy):
            print("Enough data: " + str(self.check_enough_data()))
            print("Far enough: " + str(self.check_far_enough_in_past(self.last_buy)))
            return False

        if not self.check_if_last_sample_is_outlier():
            print("Not an outlier!")
            return False

        print("Buying!")
        return True

    def check_should_sell(self):
        super().check_should_sell()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_sell):
            return False

        if not self.check_if_last_sample_is_outlier():
            return False

        return True

    def determine_buy_volume(self, price, holdings, account_balance):
        volume = 2
        trans = TransationRecord(
            'buy', datetime.now(), 'XBT', price, volume, price * volume, 'JPY')
        self.last_buy = trans
        return volume

    def determine_sell_volume(self, price, holdings, account_balance):
        volume = 2
        trans = TransationRecord(
            'sell', datetime.now(), 'XBT', price, volume, price * volume, 'JPY')
        self.last_sell = trans
        return volume

    # Non interface methods
    def last_price(self):
        return self.data[0].price

    def check_enough_data(self):
        three_days_ago = datetime.now() - timedelta(days=3)
        min_date = self.data[-1].date
        old_enough = min_date < three_days_ago
        enough = len(self.data) >= 500
        return old_enough and enough

    def check_far_enough_in_past(self, transaction):
        min_wait = timedelta(hours=3)
        if transaction is None:
            return True
        else:
            return transaction.date < datetime.now() - min_wait

    def recent_prices(self):
        min_date = datetime.now() - self.comparison_window
        return [sample for sample in self.data if sample.date > min_date]

    def recent_mean(self):
        prices = [sample.price for sample in self.recent_prices()]
        return np.array(prices).mean()

    def recent_stddev(self):
        prices = [sample.price for sample in self.recent_prices()]
        return np.array(prices).std()

    def passed_local_min(self):
        prices = [sample.price for sample in self.recent_prices()]
        if len(prices) < 5:
            return False
        was_falling = prices[2] < prices[3] < prices[4]
        is_rising = prices[0] > prices[1] > prices[2]
        return was_falling and is_rising

    def passed_local_max(self):
        prices = [sample.price for sample in self.recent_prices()]
        if len(prices) < 5:
            return False
        was_rising = prices[2] > prices[3] > prices[4]
        is_falling = prices[0] < prices[1] < prices[2]
        return was_rising and is_falling

    def check_if_last_sample_is_outlier(self):
        prices  = np.array([sample.price for sample in self.data])
        stddev = prices.std()
        mean = prices.mean()
        diff = abs(self.last_price() - mean)
        return diff > stddev * self.sigma


