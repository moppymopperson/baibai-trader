#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An immutable object representing a buy or sell transation
"""
from collections import namedtuple

"""
Representa a single but or sell transation

Parameters
----------
type: string
    'buy' or 'sell'

date: datetime
    The date and time at which the transation was made

currency: string
    The ticker symbol of the purchased currency (XBT, ETH)

price: float
    The cost of a single unit at the time of sale in the `price_currency`

shares: float
    The number of shares purchased. Multiply with the price to get the total

total: float
    The sum total cost. Also the product of `price` and `shares`

price_currency: string
    The currency the price is given in. Typically USD or JPY, but could be
    another crypto currency as well, such as when buying Bitcoin with Etherium.
"""
fields = 'type date currency price shares total price_currency'
TransationRecord = namedtuple('TransactionRecord', fields)
