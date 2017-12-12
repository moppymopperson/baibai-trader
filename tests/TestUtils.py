

from unittest import TestCase
from datetime import datetime
from nose.tools import raises

from bitbaibai.utils import read_days_of_price_history, read_price_history
from bitbaibai.utils import parse_price_sample

test_log = 'tests/test_log.log'
line = '2017-12-11 13:00:46 : XBT USD = 16200.00000'


class TestLogUtils(TestCase):

    def test_parse_sample_price(self):
        price = parse_price_sample(line)
        assert price.price == 16200.0

    def test_parse_sample_date(self):
        price = parse_price_sample(line)
        assert price.date == datetime(2017, 12, 11, 13, 0, 46)

    def test_parse_sample_cutrency(self):
        price = parse_price_sample(line)
        assert price.currency == 'XBT'

    def test_parse_sample_price_currency(self):
        price = parse_price_sample(line)
        assert price.price_currency == 'USD'

    def test_read_all_prices(self):
        prices = read_price_history(test_log)
        assert len(prices) == 8

    def test_read_to_date(self):
        after = datetime(2017, 12, 11, 12, 57)
        prices = read_price_history(test_log, after)
        assert len(prices) == 4

    def test_read_max_entries(self):
        prices = read_price_history(test_log, max_samples=3)
        assert len(prices) == 3

    def test_max_first(self):
        after = datetime(2017, 12, 11, 12, 57)
        max_number = 1
        prices = read_price_history(test_log, after, max_number)
        assert len(prices) == 1

    def test_date_first(self):
        after = datetime(2017, 12, 11, 12, 57)
        max_number = 8
        prices = read_price_history(test_log, after, max_number)
        assert len(prices) == 4

    def test_read_days_price_history(self):
        starting = datetime(2017, 12, 13, 12, 57)
        prices = read_days_of_price_history(
            test_log, 2, starting_from=starting)
        print([price.price for price in prices])
        assert len(prices) == 4

    @raises(ValueError)
    def test_no_neg_values(self):
        max_number = -3
        read_price_history(test_log, max_samples=max_number)

    @raises(TypeError)
    def test_date_type(self):
        read_price_history(test_log, 5)
