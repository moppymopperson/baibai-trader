#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime, timedelta
from unittest import TestCase
from bitbaibai import ErikAlgorithm, PriceSample, TransationRecord


class TestErikAlgorithm(TestCase):

    def setUp(self):
        self.alg = ErikAlgorithm(1, 1, 3.0)

    def sample_price(self, price=15.0, date=datetime.now()):
        return PriceSample(price, date, 'XBT', 'USD')

    def sample_data(self, n, sigma, mu):
        values = np.random.normal(mu, sigma, n)
        values[values >= 3 * sigma + mu] = mu
        dt = timedelta(minutes=10)
        data = []
        for i in range(n):
            price = values[i]
            date = datetime.now() - dt * i
            sample = PriceSample(price, date, 'XBT', 'USD')
            data.append(sample)
        return data

    def test_sets_sigma(self):
        alg = ErikAlgorithm(5, 5, 4.0)
        assert alg.sigma == 4.0

    def test_sets_sigma_to_float(self):
        alg = ErikAlgorithm(5, 5, 4.0)
        assert isinstance(alg.sigma, float)

    def test_sets_buy_sell_volume(self):
        alg = ErikAlgorithm(5, 6, 4.0)
        assert alg.buy_volume == 5
        assert alg.sell_volume == 6

    def test_sets_volumes_to_floats(self):
        alg = ErikAlgorithm(int(2), int(4), 4.0)
        assert isinstance(alg.buy_volume, float)
        assert isinstance(alg.sell_volume, float)
    
    def test_sets_min_samples(self):
        alg = ErikAlgorithm(5, 6, 4.0, min_samples=100)
        assert alg.min_samples == 100

    def test_sets_min_days(self):
        alg = ErikAlgorithm(5, 6, 4.0, min_days_of_data=4)
        assert alg.min_days_of_data == 4

    def test_converts_min_smaples_to_int(self):
        alg = ErikAlgorithm(5, 6, 4.0, min_samples=10.5)
        assert alg.min_samples == 10

    def test_last_buy_sell_start_none(self):
        assert self.alg.last_buy is None
        assert self.alg.last_sell is None

    def test_starts_empty_data(self):
        assert len(self.alg.data) == 0

    def test_appends_data_when_received(self):
        self.alg.process_data([self.sample_price()])
        assert len(self.alg.data) == 1

    def test_does_not_overwrite_data(self):
        self.alg.process_data([self.sample_price()])
        self.alg.process_data([self.sample_price(), self.sample_price()])
        assert len(self.alg.data) == 3

    def test_new_samples_at_index_0(self):
        self.alg.process_data(self.sample_data(3, 1, 10))
        dates = [price.date for price in self.alg.data]
        assert dates[0] > dates[1] > dates[2]

    def test_dont_buy_data_too_new(self):
        date = datetime.now() - timedelta(days=2)
        self.alg.process_data([self.sample_price(date)])
        assert self.alg.check_should_buy() is False

    def test_dont_buy_data_too_few(self):
        date = datetime.now() - timedelta(days=5)
        data = []
        for _ in range(499):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_buy() is False

    def test_dont_buy_last_buy_too_recent(self):
        self.alg.last_buy = TransationRecord(
            'buy', datetime.now(), 'XBT', 10, 5, 50, 'USD')
        date = datetime.now() - timedelta(days=5)
        data = []
        for _ in range(600):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_buy() is False

    def test_dont_buy_not_outlier(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        assert self.alg.check_should_buy() is False

    def test_dont_buy_outlier_high(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        self.alg.data.insert(0, PriceSample(9999, datetime.now(), 'XBT', 'JPY'))
        assert self.alg.check_should_buy() == False

    def test_dont_but_still_falling(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        self.alg.data.insert(0, PriceSample(100, datetime.now(), 'XBT', 'JPY'))
        assert self.alg.check_should_buy() == False

    def test_do_buy_conditions(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        self.alg.data.insert(0, PriceSample(0.2, datetime.now(), 'XBT', 'JPY'))
        self.alg.data.insert(0, PriceSample(0.1, datetime.now(), 'XBT', 'JPY'))
        self.alg.data.insert(0, PriceSample(0.2, datetime.now(), 'XBT', 'JPY'))
        self.alg.data.insert(0, PriceSample(0.3, datetime.now(), 'XBT', 'JPY'))
        assert self.alg.check_should_buy() == True

    def test_dont_sell_data_too_new(self):
        date = datetime.now() - timedelta(days=2)
        self.alg.process_data([self.sample_price(date)])
        assert self.alg.check_should_sell() is False

    def test_dont_sell_data_too_few(self):
        date = datetime.now() - timedelta(days=5)
        data = []
        for _ in range(499):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_sell() is False

    def test_dont_sell_last_sell_too_recent(self):
        self.alg.last_sell = TransationRecord(
            'sell', datetime.now(), 'XBT', 10, 5, 50, 'USD')
        date = datetime.now() - timedelta(days=5)
        data = []
        for _ in range(600):
            data.append(self.sample_price(date))
        self.alg.process_data(data)
        assert self.alg.check_should_sell() is False

    def test_dont_sell_not_outlier(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        assert self.alg.check_should_sell() == False

    def test_dont_sell_still_rising(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        self.alg.data.insert(0, PriceSample(1010, datetime.now(), 'XBT', 'JPY'))
        assert self.alg.check_should_sell() == False

    def test_do_sell_conditions(self):
        self.alg.last_buy = None
        self.alg.data = self.sample_data(1000, 1, 300)
        self.alg.data.insert(0, PriceSample(500, datetime.now(), 'XBT', 'JPY'))
        self.alg.data.insert(0, PriceSample(510, datetime.now(), 'XBT', 'JPY'))
        self.alg.data.insert(0, PriceSample(500, datetime.now(), 'XBT', 'JPY'))
        self.alg.data.insert(0, PriceSample(490, datetime.now(), 'XBT', 'JPY'))
        assert self.alg.check_should_sell() == True

    def test_set_last_buy_on_buy(self):
        self.alg.determine_buy_volume(20, 5, 1000)
        assert self.alg.last_buy is not None

    def test_set_last_sell_on_sell(self):
        self.alg.determine_sell_volume(20, 5, 1000)
        assert self.alg.last_sell is not None

    def test_no_outliers(self):
        self.alg.data = self.sample_data(1000, 1, 100)
        assert self.alg.check_if_last_sample_is_outlier() == False

    def test_outlier(self):
        self.alg.data = self.sample_data(1000, 1, 100)
        self.alg.data.insert(0, PriceSample(9999, datetime.now(), 'XBT', 'JPY'))
        assert self.alg.check_if_last_sample_is_outlier() == True

    def test_recent_prices(self):
        self.alg.comparison_window = timedelta(days=3)
        now = datetime.now()
        a = self.sample_price(5, date=now-timedelta(days=0))
        b = self.sample_price(10, date=now-timedelta(days=2))
        c = self.sample_price(15, date=now-timedelta(days=4))
        self.alg.data = [a, b, c]
        assert self.alg.recent_prices() == [a, b]

    def test_recent_mean(self):
        self.alg.comparison_window = timedelta(days=3)
        now = datetime.now()
        a = self.sample_price(5, date=now-timedelta(days=0))
        b = self.sample_price(10, date=now-timedelta(days=2))
        c = self.sample_price(15, date=now-timedelta(days=4))
        self.alg.data = [a, b, c]
        assert self.alg.recent_mean() == 7.5

    def test_recent_stddev(self):
        self.alg.comparison_window = timedelta(days=3)
        now = datetime.now()
        a = self.sample_price(10, date=now-timedelta(days=0))
        b = self.sample_price(10, date=now-timedelta(days=2))
        c = self.sample_price(15, date=now-timedelta(days=4))
        self.alg.data = [a, b, c]
        assert self.alg.recent_stddev() == 0

    def test_passed_local_min_false_data_if_no_data(self):
        self.alg.comparison_window = timedelta(days=3)
        now = datetime.now()
        a = self.sample_price(10, date=now-timedelta(days=0))
        b = self.sample_price(10, date=now-timedelta(days=2))
        c = self.sample_price(15, date=now-timedelta(days=4))
        self.alg.data = [a, b, c]
        assert self.alg.passed_local_min() is False

    def test_passed_local_min(self):
        now = datetime.now()
        a = self.sample_price(20, date=now-timedelta(hours=0))
        b = self.sample_price(16, date=now-timedelta(hours=2))
        c = self.sample_price(15, date=now-timedelta(hours=4))
        d = self.sample_price(16, date=now-timedelta(hours=6))
        e = self.sample_price(19, date=now-timedelta(hours=10))
        self.alg.data = [a, b, c, d, e]
        assert self.alg.passed_local_min() is True
    
    def test_passed_local_max_false_data_if_no_data(self):
        self.alg.comparison_window = timedelta(days=3)
        now = datetime.now()
        a = self.sample_price(10, date=now-timedelta(days=0))
        b = self.sample_price(10, date=now-timedelta(days=2))
        c = self.sample_price(15, date=now-timedelta(days=4))
        self.alg.data = [a, b, c]
        assert self.alg.passed_local_max() is False

    def test_passed_local_max(self):
        now = datetime.now()
        a = self.sample_price(10, date=now-timedelta(hours=0))
        b = self.sample_price(12, date=now-timedelta(hours=2))
        c = self.sample_price(15, date=now-timedelta(hours=4))
        d = self.sample_price(11, date=now-timedelta(hours=6))
        e = self.sample_price(7, date=now-timedelta(hours=10))
        self.alg.data = [a, b, c, d, e]
        assert self.alg.passed_local_max() is True

    def test_last_price(self):
        self.alg.data = self.sample_data(10, 5, 10)
        assert self.alg.last_price() == self.alg.data[0].price

    def test_price_is_high(self):
        self.alg.data = self.sample_data(100, 5, 100)
        self.alg.data.insert(0, self.sample_price(200))
        assert self.alg.price_is_high() == True

    def test_price_is_not_high(self):
        self.alg.data = self.sample_data(100, 5, 100)
        self.alg.data.insert(0, self.sample_price(20))
        assert self.alg.price_is_high() == False

    def test_price_is_low(self):
        self.alg.data = self.sample_data(100, 5, 100)
        self.alg.data.insert(0, self.sample_price(20))
        assert self.alg.price_is_low() == True

    def test_price_is_not_low(self):
        self.alg.data = self.sample_data(100, 5, 100)
        self.alg.data.insert(0, self.sample_price(200))
        assert self.alg.price_is_low() == False