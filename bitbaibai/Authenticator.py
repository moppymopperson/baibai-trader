#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the an abstract base class (ABC) that serves as an interface
for trading on any market.
"""
from abc import ABC, abstractmethod


class Authenticator(ABC):
    """
    An Authenticator inheriting from this class should be defined for every 
    market that we want to trade on.
    """

    @abstractmethod
    def get_current_price(self):
        """
        Get the present price of the target currency.

        Returns
        -------
        price: float
            The current price of the currency. The value returned should be in 
            units of the currency returned by `price_currency()`.
        """
        pass

    @abstractmethod
    def price_currency(self):
        """
        Specify the currency that price will be returned in. For example, when
        buying Bitcoin the price might be given in dollars (USD) or yen (JPY)

        Returns
        -------
        currency: string
            A capitalized 3 letter currency code such as USD or JPY
        """
        pass

    @abstractmethod
    def buy(self, n_shares):
        """
        Buy a certain number of the target currency. If not successful, an
        exception should be raised.

        Parameters
        ----------
        n_shares: float
            The number of coins to buy. May be fractional.
        """
        assert(n_shares > 0, "You can only buy a positive number of shares")

    @abstractmethod
    def sell(self, n_shares):
        """
        Sell a number of coins at the current market price.

        Parameters
        ----------
        n_shares: float
            The number of coins to sell. May be fractional.
        """
        assert(n_shares > 0, "You can only sell a positive number of shares")
