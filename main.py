#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Where the action happens
"""
from bitbaibai import Trader, DummyAlgorithm, PracticeAuthenticator

auth = PracticeAuthenticator(1000, 'XBT', 'USD')
algorithm = DummyAlgorithm()
trader = Trader('DummyTrader', auth, algorithm, update_interval=60.0)

trader.begin_trading()
