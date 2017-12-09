#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains an dummy algorithm that doesn't do anything. This may be
useful if you just want to collect data without making any buys or sells.
"""
from .Algorithm import Algorithm
from ..PriceSample import PriceSample


class DummyAlgorith(Algorithm):
    """
    A dummy algorithm that doesn't do anything
    """
    past_prices = []

    def process_data(self, price_samples):
        for sample in price_samples:
            self.past_prices.append(sample)

    def check_should_buy(self):
        return False

    def check_should_sell(self):
        return False

    def determine_buy_volume(self):
        pass

    def determine_sell_volume(self):
        pass
