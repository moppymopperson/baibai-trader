#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Support for the Kraken Exchange
"""
import datetime
import krakenex

from .Authenticator import Authenticator
from .PriceSample import PriceSample


class KrakenAuthenticator(Authenticator):
    """
    An authenticator that allows trading on the Kraken Exchange
    Currently only supports BitCoin/USD
    """

    def __init__(self, key_file, target_currency, account_currency):
        """
        Create a new authenticator using a key file. The keyfile should be a 
        plain text file with the key on the first line and the secret on the
        second line.

        Parameters
        ----------
        key_file: str
            The path to a plain text file containing your accounts key on the 
            first line and your secret on the second line. Make sure to keep
            this data secret!
        """
        self._api = krakenex.API()
        self._api.load_key(key_file)
        self._target_currency = target_currency
        self._account_currency = account_currency

    def get_pair(self):
        """
        Builds the pair abbreviation used by Kraken

        Returns
        -------
        pair: string
            Kraken uses the pattern X + TARGET + Z + FIAT. For example, the 
            BitCoin/USD pair is XXBTZUSD
        """
        return 'X' + self.target_currency() + 'Z' + self.price_currency()

    def price_currency(self):
        """
        Returns the purchasing currency

        Returns
        -------
        currency: string
            A capitalized 3 letter currency code such as USD or JPY
        """
        return self._account_currency

    def target_currency(self):
        """
        Get the currency being traded for

        Returns
        -------
        ticker_symbol: string
            The ticker symbol for the currency being traded, i.e. XBT for
            Bitcoin
        """
        return self._target_currency

    def get_current_price(self):
        """
        Get the present price of the target currency. 

        Returns
        -------
        price: float
            The current price of the currency. The value returned should be in 
            units of the currency returned by `price_currency()`.

        Raises
        ------
        RuntimeError
            If fetching the current price fails for some reason
        """
        super().get_current_price()

        # Query the public API
        response = self._api.query_public(
            'Depth', {'pair': self.get_pair(), 'count': '3'})

        # Check for errors
        if len(response['error']) is not 0:
            raise RuntimeError(str(response['error']))

        # Build a `PriceSample` to return
        cost = response['result'][self.get_pair()]['asks'][0][0]
        date = datetime.datetime.now()
        price = PriceSample(
            cost, date, self.target_currency(), self.price_currency())
        return price

    def get_account_balance(self):
        """
        Check the balance of the purchasing account

        Returns
        -------
        balance: float
            The current balance of the account defined by `price_currency`

        Raises
        ------
        RuntimeError
            If fetching fails for some reason
        """
        pass

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
        """
        pass

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
            If you try to buy <= 0 shares
        """
        super().buy(n_shares)
        # TODO: 

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
            If you try to sell <= 0 shares
        """
        super().sell(n_shares)
        # TODO:
