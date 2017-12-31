# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A class that retroactively applies an algorithm to log data to see how it would
have performed had it been used at that time. This is useful for evaluation the
performance of new algorithms and for checking for bugs before going live.
"""
from datetime import datetime
from .TransationRecord import TransationRecord
from .utils import read_price_history


class AlgorithmValidator:

    def __init__(self, logfile, algorithm, holdings, balance):
        self.logfile = logfile
        self.algorithm = algorithm
        self.holdings = holdings
        self.balance = balance
        self.buys = []
        self.sells = []
        self.sample_history = read_price_history(logfile)
        self.holdings_history = []
        self.balance_history = []

    def simulate_trading(self):
        self.buys = []
        self.sells = []
        self._update_history(date=self.sample_history[-1].date)

        for sample in self.sample_history:
            self.algorithm.process_data([sample])
            if self.algorithm.check_should_buy():
                buy_volume = self.algorithm.determine_buy_volume(
                    sample, self.holdings, self.balance)
                self.holdings += buy_volume
                self.balance -= sample.price * buy_volume
                record = TransationRecord('buy', sample.date, sample.currency,
                                          sample.price,
                                          buy_volume, sample.price * buy_volume, sample.price_currency)
                self.buys.append(record)
                self._update_history(date=sample.date)
            elif self.algorithm.check_should_sell():
                sell_volume = self.algorithm.determine_sell_volume(
                    sample, self.holdings, self.balance)
                self.holdings -= sell_volume
                self.balance += sell_volume * sample.price
                record = TransationRecord('sell', sample.date, sample.currency,
                                          sample.price, sell_volume, sample.price * sell_volume, sample.price)
                self.sells.append(record)
                self._update_history(date=sample.date)

    def data_pairs_for_plotting(self):
        dates = [sample.date for sample in self.sample_history]
        prices = [sample.price for sample in self.sample_history]
        buy_dates = [action.date for action in self.buys]
        buy_prices = [action.price for action in self.buys]
        sell_dates = [action.date for action in self.sells]
        sell_prices = [action.price for action in self.sells]
        balance_dates = [x[1] for x in self.balance_history]
        balance_values = [x[0] for x in self.balance_history]
        holdings_dates = [x[1] for x in self.holdings_history]
        holdings_values = [x[0] for x in self.holdings_history]

        return {
            "prices": {
                "dates": dates,
                "values": prices
            },
            "buys": {
                "dates": buy_dates,
                "values": buy_prices
            },
            "sells": {
                "dates": sell_dates,
                "values": sell_prices
            },
            "balance": {
                "dates": balance_dates,
                "values": balance_values
            },
            "holdings": {
                "dates": holdings_dates,
                "values": holdings_values
            }
        }

    def _update_history(self, date):
        self.holdings_history.append((self.holdings, date))
        self.balance_history.append((self.balance, date))
