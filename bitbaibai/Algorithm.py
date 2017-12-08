#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains an abstract base class (ABC) that serves as an interface for
any algorithm used to determine when to buy and sell.
"""
from abc import ABC, abstractmethod


class Algorithm(ABC):
    """
    All algorithms for determing when to buy and sell should inherit from this
    class.
    """

    @abstractmethod
    def process_data(self, price_samples):
        """
        This method will be called automatically when new price data becomes
        available. You should store the received price data for later processing
        if necessary.

        Parameters
        ----------
        price_samples: array of PriceSample
            An array of `PriceSample` data points
        """
        pass

    @abstractmethod
    def check_should_buy(self):
        """
        Based on the data currently availble, check if we should buy.

        Returns
        -------
        should_buy: boolean
            True if we should buy, False otherwise
        """
        pass

    @abstractmethod
    def check_should_sell(self):
        """
        Based on the data currently available, check if we should sell.

        Returns
        -------
        should_sell: boolean
            True if we should sell, False otherwise
        """

    @abstractmethod
    def determine_buy_volume(self):
        """
        This method will be automatically called when it is time to buy. Based
        on the data available, return the number of shares to buy.

        Returns
        -------
        n_shares: float
            The number of shares to buy. Maybe fractional.
        """
        pass

    @abstractmethod
    def determine_sell_volume(self):
        """
        This method will be automatically called when it is time to sell. Based
        on the data available, return the number of shares to sell.

        Returns
        -------
        n_shares: float
            The number of shares to sell
        """
        pass
