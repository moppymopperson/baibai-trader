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
        self.data = []
        self.last_buy = None
        self.last_sell = None

    def process_data(self, price_samples):
        super().process_data(price_samples)
        for sample in price_samples:
            self.data.append(sample)

    def check_should_buy(self):
        super().check_should_buy()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_buy):
            return False

    def check_should_sell(self):
        super().check_should_sell()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_sell):
            return False

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

    def check_if_last_sample_is_outlier(self):
        stddev = np.array([sample.price for sample in self.data]).std()
        plt.plot([s.price for s in self.data])
        plt.show()
        print("STDDEV: " + str(stddev))
        print("LAST: " + str(self.data[-1].price))
        bigger = abs(self.data[-1].price) > stddev
        print("BIGGER: " + str(bigger))
        return False

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
