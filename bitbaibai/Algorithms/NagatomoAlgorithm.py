#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains an `Algorithm` developed by Yuuji Nagatomo for automatically
determing when to buy and sell virtual currencies.
"""
from .Algorithm import Algorithm


class NagatomoAlgorithm(Algorithm):
    """
    長友さん特製のアルゴリズム！
    """

    def process_data(self, data):
        super().process_data(data)
        # TODO:

    def check_should_buy(self):
        super().check_should_buy()
        # TODO:

    def check_should_sell(self):
        super().check_should_sell()
        # TODO:

    def determine_buy_volume(self, price, holdings, account_balance):
        super().determine_buy_volume(price, holdings, account_balance)
        # TODO:

    def determine_sell_volume(self, price, holdings, account_balance):
        super().determine_sell_volume(price, holdings, account_balance)
        # TODO:
