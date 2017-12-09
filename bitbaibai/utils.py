#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains various helpful utilities that don't have a home all their own
"""
import logging


def build_logger(identifier, filename, level=logging.INFO, output_console=True):
    """
    Gets (or creates if nonexistent) a file logger that also logs out to the
    stdout and stderror. Log entries will be timestamped as well.
    """
    l = logging.getLogger(identifier)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(filename, mode='w')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

    if output_console:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.addHandler(streamHandler)

    return l
