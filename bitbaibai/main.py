#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Where the action happens
"""
from .Trader import Trader
from .Algorithms import DummyAlgorithm
from .Markets import PracticeAuthenticator

starting_balance = 1000
auth = PracticeAuthenticator()
