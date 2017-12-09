#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementation for an automated trader that operates on a single market and 
currency.
"""
import threading
from .utils import build_logger


class Trader:
    """
    The `Trader` class owns an `Authenticator` and an `Algorithm`. It uses the
    authenticator to periodically check the state of the market and passes the
    results to its algorithm to make a decision about what to do next. Buying
    and selling actions are delegated to the authenticator.
    """

    def __init__(self, name, authenticator, algorithm,
                 update_interval=300.0, output_console=True):
        """
        Create a new `Trader` with a specific `Authenticator` and `Algorithm`

        Parameters
        ----------
        name: string or None
            The name given to the `Trader` will be used to generate logs.
            Reusing a name will essentially restart a terminated trader by
            continuing the logs where the previous left off.

        authenticator: instance of `Authenticator`
            The authenticator responsible for retrieving market data and place
            buy/sell orders

        algorithm: instance of `Algorithm`
            The algorithm that will be responsible for determing if it's time 
            to buy or sell

        update_interval: float (seconds)
            How frequency the market price is checked and a new decision is 
            made. Units are in seconds. Defaults to 300 seconds (5 minutes).

        output_console: boolean (default True)
            Determines if logs will be printed to the console in addition to 
            written to disk. Making this False is nice for unit testing.
        """
        self.name = name
        self.authenticator = authenticator
        self.algorithm = algorithm
        self.update_interval = float(update_interval)
        self.is_running = False
        self.thread = threading.Timer(
            self.update_interval, self.perform_one_cycle)

        self.log = build_logger(
            'TraderInfo', 'debug_log.log', output_console=output_console)
        self.trade_log = build_logger(
            'TradeActivity', 'trade_records.log', output_console=output_console)
        self.price_log = build_logger(
            'TradePrice', 'price_log.log', output_console=output_console)

    def begin_trading(self):
        """
        Begin polling the market and trading
        """
        self.thread.start()
        self.is_running = True
        self.log.info('Began trading')

    def stop_trading(self):
        """
        Stop trading immediately
        """
        self.thread.cancel()
        self.is_running = False
        self.log.info('Stop trading')

    def perform_one_cycle(self):
        """
        Get the market price, provide the data to the algorithm, make a decision
        about what to do, and either buy or sell if appropriate. This is done in
        a sychronous manner. 
        """
        # Checking price
        try:
            price = self.authenticator.get_current_price()
            self.log.info('Received price update: %s', price)
            self.price_log.info('X%sZ%s = %s', self.authenticator.target_currency(),
                                self.authenticator.price_currency(),
                                price.price)

        except Exception as e:
            self.log.error('Failed to get price with error: %s', e)
            return

        self.algorithm.process_data([price])

        # Buying
        if self.algorithm.check_should_buy():

            balance = self.authenticator.get_account_balance()
            holdings = self.authenticator.get_holdings()
            volume = self.algorithm.determine_buy_volume(
                price, holdings, balance)

            try:
                self.log.debug('Trying to buy %s shares at %s', volume, price)
                self.authenticator.buy(volume)
                self.trade_log.info('Bought %s shares of %s at %s', volume,
                                    self.authenticator.target_currency(), price)
            except Exception as e:
                self.log.error('Failed to buy with error: %s', e)

        # Selling
        elif self.algorithm.check_should_sell():

            balance = self.authenticator.get_account_balance()
            holdings = self.authenticator.get_holdings()
            volume = self.algorithm.determine_sell_volume(
                price, holdings, balance)

            try:
                self.log.debug('Trying to sell %s shares at %s', volume, price)
                self.authenticator.sell(volume)
                self.trade_log.info('Sold %s shares of %s at %s', volume,
                                    self.authenticator.target_currency(), price)
            except Exception as e:
                self.log.error('Failed to sell with error: %s', e)
