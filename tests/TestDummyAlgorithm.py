#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the dummy algorithm to make sure that it won't accidentally spend money 
and to ensure that fulfills the Algorithm interface 
"""
from unittest import TestCase
from bitbaibai import DummyAlgorithm


class TestDummyAlgorith(TestCase):

    def setUp(self):
        self.alg = DummyAlgorithm()

    def test_no_data_at_beginning(self):
        assert self.alg.past_prices == []

    def test_process_data(self):
        self.alg.process_data([1])
        self.alg.process_data([2, 3])
        assert self.alg.past_prices == [1, 2, 3]

    def test_should_buy_always_false(self):
        assert self.alg.check_should_buy() == False

    def test_should_sell_always_false(self):
        assert self.alg.check_should_sell() == False
