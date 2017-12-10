#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains various helpful utilities that don't have a home all their own
"""
import os
import logging


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
