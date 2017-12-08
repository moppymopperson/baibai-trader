#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Authenticator(ABC):

    @abstractmethod
    def get_current_price():
        pass

    @abstractmethod
    def buy(n_shares):
        assert(n_shares > 0, "You can only buy a positive number of shares")
        

    @abstractmethod
    def sell(n_shares):
        assert(n_shares > 0, "You can only sell a positive number of shares")