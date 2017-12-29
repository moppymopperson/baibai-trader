#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run an algorithm on past data to validate its operation
"""
from bitbaibai import AlgorithmValidator, ErikAlgorithm

# Define the algorithm to test
buy_volume = 500.0
sell_volume = 500.0
algorithm = ErikAlgorithm(buy_volume, sell_volume, min_days_of_data=1)

# Create a an instance of `AlgorithmValidator`
holdings = 50.0
balance = 5000.0
price_log = 'log_files/ErikPracticeTrader_price_log.log'
validator = AlgorithmValidator(price_log, algorithm, holdings, balance)

# Run validation and plot the results
validator.simulate_trading(draw=True)
