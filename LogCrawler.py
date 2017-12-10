#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for extracting data from logs
"""
from file_read_backwards import FileReadBackwards

def extract_date(line):
    date_text = line.split(' ', 1)[0]
    print(date_text)
    
with FileReadBackwards("log_files/DummyTrader_debug.log", encoding="utf-8") as frb:
    for l in frb:
         extract_date(l)

