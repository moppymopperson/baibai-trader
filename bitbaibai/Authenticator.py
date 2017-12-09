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
    def target_currency(self):
        """
        Get the currency being traded for

        Returns
        -------
        ticker_symbol: string
            The ticker symbol for the currency being traded, i.e. BTC for
            Bitcoin or ETC for Etherium.
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
    def get_current_price(self):
        """
        Get the present price of the target currency. You should throw an
        exception if unable to get the price. 

        DO NOT return a value if the price can't be retrieved, as that could 
        result in unintended transactions being triggered.

        Returns
        -------
        price: float
            The current price of the currency. The value returned should be in 
            units of the currency returned by `price_currency()`.

        Raises
        ------
        RuntimeError
            If fetching the current price fails for some reason

        RequestException
            If there is a networking problem
        """
        pass

    @abstractmethod
    def get_account_balance(self):
        """
        Check the balance of the currency used for purchasing, typically a fiat 
        currency like USD or JPY.

        Returns
        -------
        balance: float
            The current balance of the purchasing account

        Raises
        ------
        RuntimeError
            If fetching fails for some reason

        RequestException
            If there is a networking problem
        """
        pass

    @abstractmethod
    def get_holdings(self):
        """
        Return the amount of target currency currently availble for selling. 
        The units of the currency (BTC, ETC, etc.) can be checked with the 
        `target_currency` method.

        Returns
        -------
        holdings: float
            The number of coins in the 

        Raises
        ------
        RuntimeError
            If fetching fails for some reason

        RequestException
            If there is a networking problem
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

        Raises
        ------
        RuntimeError
            If purchasing fails for some reason

        ValueError
            If you try to buy 0 or fewer shares
        """
        if n_shares <= 0:
            raise ValueError("You can only buy a positive number of shares")

    @abstractmethod
    def sell(self, n_shares):
        """
        Sell a number of coins at the current market price.

        Parameters
        ----------
        n_shares: float
            The number of coins to sell. May be fractional.

        Raises
        ------
        RuntimeError
            If selling fails for some reason

        ValueError
            If you try to sell 0 or fewer shares
        """
        if n_shares <= 0:
            raise ValueError("You can only sell a positive number of shares")
