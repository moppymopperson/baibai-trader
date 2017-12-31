#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains various helpful utilities that don't have a home all their own
"""
import os
import logging
from file_read_backwards import FileReadBackwards
from dateutil.parser import parse
from datetime import datetime, timedelta

from .PriceSample import PriceSample


def build_logger(identifier, filename, level=logging.INFO, output_console=True):
    """
    Gets (or creates if nonexistent) a file logger that also logs out to the
    stdout and stderror. Log entries will be dateed as well.
    """
    log_folder = 'log_files'
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    l = logging.getLogger(identifier)
    formatter = logging.Formatter(
        '%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
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
    """
    Parse a single line of a price log file into a `PriceSample` object

    Parameters
    ----------
    line: string
        A string matching the following format
        '2017-12-11 13:00:46 : XBT USD = 16200.00000'

    Returns
    -------
    price_sample: `PriceSample`
        A `PriceSample` object with info about the price and time it was
        recorded at.
    """
    words = line.split(' ')
    date = parse(words[0] + ' ' + words[1])
    currency = words[3]
    price_currency = words[4]
    price = float(words[6])
    return PriceSample(price, date, currency, price_currency)


def read_price_history(log_file, after_date=None, max_samples=None):
    """
    Read the price history of a currency from a log file. By specifying optional
    arguments it is possible to read only data after a certain date or go 
    backwards in time until you reach a certain number of samples. Specifying
    both will end at whichever condition is met first.

    Parameters
    ----------
    log_file: string
        Path to the log file to read

    after_date:
        The earliest date at which you wish samples to be returned from

    max_samples: 
        The maximum number of prices samples you wish to be returned

    Returns
    -------
    samples: list of PriceSample
        A list of `PriceSample` objects with the first element being the most
        recent data and the last element being the data furthest in the past.

        Note that the samples will likely not be equally spaced, so it may be
        important for you algorithm to use the `date` attribute of the returned
        samples to check when the sample was taken, especially if you want to
        perform any kind of interpolation.
    """
    if max_samples is not None and max_samples < 0:
        raise ValueError('max_samples must be >= 0')

    if after_date is not None and not isinstance(after_date, datetime):
        raise TypeError('after_date must be a datetime object')

    samples = []
    with FileReadBackwards(log_file, encoding="utf-8") as frb:
        for line in frb:
            sample = parse_price_sample(line)
            if after_date is not None and sample.date < after_date:
                return samples
            samples.append(sample)
            if max_samples is not None and len(samples) >= max_samples:
                return samples
    return samples


def read_days_of_price_history(log_file, days, starting_from=datetime.now()):
    """
    Reads the previous x days of data from a price log. This is a convenience
    method that calls `read_price_history` under the hood

    Parameters
    ----------
    log_file: string
        Path to the log file to be read from

    days: float or int
        The number of days into the past for which to retrieve data

    starting_from: datetime (defaults to now())
        The date from which to start counting back. Typically you will want this
        to be the present date, so the default argument will be sufficient.

    Returns
    -------
    samples: list of PriceSample
        A list of `PriceSample` objects with the first element being the most
        recent data and the last element being the data furthest in the past.

        Note that the samples will likely not be equally spaced, so it may be
        important for you algorithm to use the `date` attribute of the returned
        samples to check when the sample was taken, especially if you want to
        perform any kind of interpolation.
    """
    delta = timedelta(days=days)
    then = starting_from - delta
    return read_price_history(log_file, after_date=then)
