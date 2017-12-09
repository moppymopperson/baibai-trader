#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains an abstract base class (ABC) that serves as an interface for
any algorithm used to determine when to buy and sell.
"""
from abc import ABC, abstractmethod
from .PriceSample import PriceSample


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
        assert all(isinstance(item, PriceSample) for item in price_samples), \
            "Not all items in price_samples were `PriceSample` objects"

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
    def determine_buy_volume(self, price, holdings, account_balance):
        """
        This method will be automatically called when it is time to buy. Based
        on the data available, return the number of shares to buy.

        Parameters
        ----------
        price: PriceSample
            Info about the going price of the traded asset

        holdings: float
            The number of shares currently owned

        account_balance: float
            The amount of currency availble to use for purchasing

        Returns
        -------
        n_shares: float
            The number of shares to buy. May be fractional.
        """
        pass

    @abstractmethod
    def determine_sell_volume(self, price, holdings, account_balance):
        """
        This method will be automatically called when it is time to sell. Based
        on the data available, return the number of shares to sell.

        Parameters
        ----------
        price: PriceSample
            Info about the cost of the asset

        holdings: float
            The number of shares currently owned

        account_balance: float
            The balance currently available in the account

        Returns
        -------
        n_shares: float
            The number of shares to sell. May be fractional.
        """
        pass
