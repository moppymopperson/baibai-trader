#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains various helpful utilities that don't have a home all their own
"""
import os
import logging
from file_read_backwards import FileReadBackwards
from dateutil.parser import parse
from datetime import datetime

from .PriceSample import PriceSample


def build_logger(identifier, filename, level=logging.INFO, output_console=True):
    """
    Gets (or creates if nonexistent) a file logger that also logs out to the
    stdout and stderror. Log entries will be timestamped as well.
    """
    log_folder = 'log_files'
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    l = logging.getLogger(identifier)
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_folder + '/' + filename, mode='a')
    fileHandler.setFormatter(formatter)

    if output_console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.addHandler(streamHandler)

    l.addHandler(fileHandler)
    l.setLevel(level)
    return l

def parse_price_sample(line):
    words = line.split(' ')
    date = parse(words[0] + ' ' + words[1])
    currency = words[3]
    price_currency = words[4]
    price = float(words[6])
    return PriceSample(price, date, currency, price_currency)

def read_price_history(log_file, after_date=None, max_samples=None):
    if max_samples is not None and max_samples < 0:
        raise ValueError('max_samples must be >= 0')

    if after_date is not None and not isinstance(after_date, datetime):
        raise TypeError('after_date must be a datetime object')
        
    samples = []
    with FileReadBackwards(log_file, encoding="utf-8") as frb:
        for line in frb:
            sample = parse_price_sample(line)
            if after_date is not None and sample.timestamp < after_date:
                return samples
            samples.append(sample)
            if max_samples is not None and len(samples) >= max_samples:
                return samples
    return samples

def read_days_of_price_history(log_file, days, starting_from=datetime.now()):
    delta = datetime.timedelta(days=days)
    then = starting_from - delta
    return read_price_history(log_file, after_date=then)