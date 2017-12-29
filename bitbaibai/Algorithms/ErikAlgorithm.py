#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains an `Algorithm` developed by Erik Hornberger for automatically
determing when to buy and sell virtual currencies.
"""
import numpy as np
from datetime import datetime, timedelta
from .Algorithm import Algorithm
from ..TransationRecord import TransationRecord


class ErikAlgorithm(Algorithm):

    def __init__(self, buy_volume, sell_volume, sigma=3, min_samples=500,
                 min_days_of_data=3, min_hours_between_trades=3, recent_days=3):
        """
        Parameters
        ----------

        buy_volume:
            The amount to of money to spend on each purchase. The units are of
            the currency being used to make the purchase, not of the currency
            being purchased. For example, if `buy_volume` is set to 100 and the
            pair is XBT/USD, then $100 of bitcoin will be bought on each buy.

        sell_volume:
            The amount value of the asset to the sold on each sale The units are
            of the currency being used to make the purchase, not of the currency
            being sold. For example, if `sell_volume` is set to 100 and the pair
            is XBT/USD, then $100 worth of bitcoin will be sold on each sale.

        sigma: float
            Used to set a threshold for determing outliers. Nothing will be
            bought or sold unless the price is more than sigma times times the
            standard deviation greater or less than the mean

        min_samples: int
            The minimum of price samples to collect before starting to run
            trading logic. If there are too few samples values like the mean and
            standard deviation won't be meaningful and could lead to unwise buys
            and sells.

        min_days_of_data: number
            The minimum number of days of data to collect before beginning to
            trade. If data is collected at very short intervals, it is possible
            to excee `min_samples` in a short period of time, but you may wish
            to wait until more data has been collected first. In that case, use
            this variable. 

        min_hours_betwee_trades: number
            This value is used to prevent rapid successive buys or sells when
            the price continually meets the buy/sell criterion.

        recent_days: number
            The number of days that are considered recent when using methods
            as `recent_prices`, `recent_mean`, and `recent_stddev`.
        """
        self.sigma = float(sigma)
        self.recent_days = timedelta(days=recent_days)
        self.data = []
        self.buy_volume = float(buy_volume)
        self.sell_volume = float(sell_volume)
        self.min_samples = int(min_samples)
        self.min_days_of_data = min_days_of_data
        self.min_hours_between_trades = min_hours_between_trades
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
            return False
        if not self.check_if_last_sample_is_outlier() or not self.price_is_low():
            return False
        if not self.passed_local_min():
            return False
        return True

    def check_should_sell(self):
        super().check_should_sell()
        if not self.check_enough_data() or not self.check_far_enough_in_past(self.last_sell):
            return False
        if not self.check_if_last_sample_is_outlier() or not self.price_is_high():
            return False
        if not self.passed_local_max():
            return False
        return True

    def determine_buy_volume(self, price, holdings, account_balance):
        super().determine_buy_volume(price, holdings, account_balance)
        if self.buy_volume > account_balance:
            return 0

        volume = self.buy_volume / price.price
        trans = TransationRecord(
            'buy', price, 'XBT', price.price, volume, price.price * volume, 'JPY')
        self.last_buy = trans
        return volume

    def determine_sell_volume(self, price, holdings, account_balance):
        super().determine_sell_volume(price, holdings, account_balance)
        if self.sell_volume > holdings * price.price:
            return False
        volume = self.sell_volume / price.price
        trans = TransationRecord(
            'sell', datetime.now(), 'XBT', price.price, volume, price.price * volume, 'JPY')
        self.last_sell = trans
        return volume

    # Non interface methods

    def last_price(self):
        return self.data[0].price

    def check_enough_data(self):
        three_days_ago = datetime.now() - timedelta(days=self.min_days_of_data)
        min_date = self.data[-1].date
        old_enough = min_date < three_days_ago
        enough = len(self.data) >= self.min_samples
        return old_enough and enough

    def check_far_enough_in_past(self, transaction):
        min_wait = timedelta(hours=self.min_hours_between_trades)
        if transaction is None:
            return True
        else:
            return transaction.date < datetime.now() - min_wait

    def recent_prices(self):
        min_date = datetime.now() - self.recent_days
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
        prices = np.array([sample.price for sample in self.data])
        stddev = prices.std()
        mean = prices.mean()
        diff = abs(self.last_price() - mean)
        return diff > stddev * self.sigma

    def price_is_high(self):
        return self.last_price() > self.recent_mean()

    def price_is_low(self):
        return self.last_price() < self.recent_mean()
