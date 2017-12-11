

from unittest import TestCase
from datetime import datetime
from nose.utils import raises

from bitbaibai.utils import read_price_history, parse_price_sample

class TestLogUtils(TestCase):

    def test_parse_sample_price(self):
        line = “”
        price = parse_price_sample(line)
        assert price.price == 5.0

    def test_parse_sample_date(self):
        line = “”
        price = parse_price_sample(line)
        assert price.timestamp == datetime()

    def test_parse_sample_cutrency(self):
        line = “”
        price = parse_price_sample(line)
        assert price.currency == “ABC”

    def test_parse_sample_price_currency(self):
        line = “”
        price = parse_price_sample(line)
        assert price.price_currency == “XYZ”

    def test_read_all_prices(self):
        test_log = “”
        prices = read_price_history(test_log)
        assert len(prices) == 4

    def test_read_to_date(self):
        test_log = “”
        after = datetime()
        prices = read_price_history(test_log, after)
        assert len(prices) == 3

    def test_read_max_entries(self):
        test_log = “”
        max_number = 3
        prices = read_price_history(test_log, max_number)
        assert len(prices) == 3

    def test_max_first(self):
        test_log = “”
        after = datetime()
        max_number = 1
        prices = read_price_history(test_log, after, max_number)
        assert len(prices) == 1

    def test_max_first(self):
        test_log = “”
        after = datetime()
        max_number = 3
        prices = read_price_history(test_log, after, max_number)
        assert len(prices) == 2

    @raises(ValueError)
    def test_no_neg_values(self):
        test_log = “”
        max_number = -3
        read_price_history(test_log, max_number)


    
