#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Where the action happens
"""
import time
from baibaitrader import Trader, ErikAlgorithm, PracticeAuthenticator

auth = PracticeAuthenticator(10000, 'XBT', 'USD')
algorithm = ErikAlgorithm(500, 500, min_days_of_data=1)

trader = Trader('ErikPracticeTrader', auth, algorithm, update_interval=60.0)
trader.begin_trading()
print("Began trading")
