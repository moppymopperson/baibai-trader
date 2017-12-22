# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A class that retroactively applies an algorithm to log data to see how it would
have performed had it been used at that time. This is useful for evaluation the
performance of new algorithms and for checking for bugs before going live.
"""

class AlgorithmTester:

    def __init__(self, logfile, algorithm):
