#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Where the action happens
"""
import time
from bitbaibai import Trader, DummyAlgorithm, PracticeAuthenticator, DummyAuthenticator

# auth = PracticeAuthenticator(1000, 'XBT', 'USD')
auth = DummyAuthenticator()
auth.start_server()

time.sleep(1)
algorithm = DummyAlgorithm()

trader = Trader('DummyTrader', auth, algorithm, update_interval=60.0)
trader.begin_trading()
print("Began trading")
