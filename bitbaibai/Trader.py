#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementation for an automated trader that operates on a single market and 
currency.
"""
import threading
import logging
logging.basicConfig(filename='trader.log',
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)


class Trader:
    """
    The `Trader` class owns an `Authenticator` and an `Algorithm`. It uses the
    authenticator to periodically check the state of the market and passes the
    results to its algorithm to make a decision about what to do next. Buying
    and selling actions are delegated to the authenticator.
    """

    def __init__(self, authenticator, algorithm, update_interval=300.0):
        """
        Create a new `Trader` with a specific `Authenticator` and `Algorithm`

        Parameters
        ----------
        authenticator: instance of `Authenticator`
            The authenticator responsible for retrieving market data and place
            buy/sell orders

        algorithm: instance of `Algorithm`
            The algorithm that will be responsible for determing if it's time 
            to buy or sell

        update_interval: float (seconds)
            How frequency the market price is checked and a new decision is 
            made. Units are in seconds. Defaults to 300 seconds (5 minutes).
        """
        self.authenticator = authenticator
        self.algorithm = algorithm
        self.update_interval = float(update_interval)
        self.is_running = False

    def begin_trading(self):
        """
        Begin polling the market and trading
        """
        self.thread = threading.Timer(
            self.update_interval, self.perform_one_cycle)
        self.thread.start()
        self.is_running = True

    def stop_trading(self):
        """
        Stop trading immediately
        """
        self.thread.cancel()
        self.is_running = False

    def perform_one_cycle(self):
        """
        Get the market price, provide the data to the algorithm, make a decision
        about what to do, and either buy or sell if appropriate. This is done in
        a sychronous manner. 
        """
        # Checking price
        price = self.authenticator.get_current_price()
        logging.info('Received price update: %s', price)
        self.algorithm.process_data([price])

        # Buying
        if self.algorithm.check_should_buy():
            volume = self.algorithm.determine_buy_volume()
            try:
                logging.debug('Trying to buy %s shares at %s', volume, price)
                self.authenticator.buy(volume)
            except Exception as e:
                logging.error('Failed to buy with error: %s', e)

        # Selling
        if self.algorithm.check_should_sell():
            volume = self.algorithm.determine_sell_volume()
            try:
                logging.debug('Trying to sell %s shares at %s', volume, price)
                self.authenticator.sell(volume)
            except Exception as e:
                logging.error('Failed to sell with error: %s', e)
