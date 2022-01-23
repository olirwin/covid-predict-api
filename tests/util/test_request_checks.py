import unittest
import pytest

from util.request_checks import *


class RequestChecksTest(unittest.TestCase) :

    def test_check_dates_order_returns_true_when_ok(self) :
        resp = check_dates_order(date(2022, 1, 1),
                                 date(2022, 2, 1))
        self.assertTrue(resp, "Date order should be accepted")

    def test_check_dates_order_returns_false_on_error(self) :
        resp = check_dates_order(date(2022, 2, 1),
                                 date(2022, 1, 1))
        self.assertFalse(resp, "Date order should be refused")

    def test_start_date(self) :
        self.assertTrue(check_start_date(date(2022, 1, 1)), "Date should be accepted")
        self.assertFalse(check_start_date(date(2020, 5, 1)), "Date should be refused")

    def test_check_end_date(self) :
        self.assertTrue(check_end_date(date(2022, 1, 1)), "Date should be accepted")
        self.assertFalse(check_end_date(date.today() + timedelta(days = 120)), "Date should be refused")

    def test_check_predict_start(self) :
        self.assertTrue(check_predict_start(date.today() - timedelta(days = 2)), "Date should be accepted")
        self.assertFalse(check_predict_start(date.today() - timedelta(days = 10)), "Date should be refused")

    def test_check_region(self) :
        self.assertTrue(check_region("FRA"), "Region should be accepted")
        self.assertFalse(check_region("75"), "Region should be refused")

    def test_check_all_returns_empty_list_when_ok(self) :
        start = date(2022, 1, 1)
        end = date(2022, 1, 10)

        l = check_all(start, end, "FRA")

        self.assertIsNotNone(l, "Returned object should not be none")
        self.assertEqual(0, len(l), "Returned list should be empty")

    def test_check_all_returns_filled_list_when_ko(self) :
        start = date(2015, 1, 1)
        end = date(2014, 1, 10)

        l = check_all(start, end, "77", prediction = True)

        self.assertEqual(4, len(l), "List should be full")
