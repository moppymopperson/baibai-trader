#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains the declaration for a data structure that holds info about 
the price of a currency at a certain time
"""
from collections import namedtuple

"""
An immutable tuple holding data about the price of a currency at some point in 
time

Parameters
----------
    price: float
        The cost of the currency in units of `price_currency`
        
    timestamp: datetime
        The time at which this data point was recorded
        
    currency: string
        The ticker symbol for currency in question, e.g. BTC for Bitcoin.
        
    price_currency: string
        The symbol for currency the price is given in, e.g. USD or JPY 
"""
PriceSample = namedtuple(
    "PriceSample", "price timestamp currency price_currency")
