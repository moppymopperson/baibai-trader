#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for extracting data from logs
"""
from file_read_backwards import FileReadBackwards
from dateutil.parser import parse

def extract_date(line):
    date_text = line.split(' ', 1)[0]
    return parse(date_text)
    
samples = []
with FileReadBackwards("log_files/DummyTrader_debug.log", encoding="utf-8") as frb:
    for l in frb:
         date = extract_date(l)
         words = line.split(' ')
         currency = words[3]
         price_currency = words[4]
         price = float(words[5])
         sample = PriceSample(price, date, currency, price_currency)
         samples.append(sample)


