import unittest

import pandas as pd
import pytest

from unittest.mock import patch
from util.data_retrieval import fetch_data, get_nation_data, get_region_data


class DataRetrievalTest(unittest.TestCase) :

    def setUp(self) -> None :
        self.nation_df = pd.read_csv("data/test_nation_df.csv", index_col = 0, sep = ";")
        self.region_df = pd.read_csv("data/test_region_df.csv", index_col = 0, dtype = {"dep" : "object"}, sep = ";")

    def test_fetch_data_returns_dataframe(self) :
        with patch("util.data_retrieval.requests.request") as mocked_get :
            with open("data/test_nation_df.csv", "rb") as f :
                data = f.read()
            mocked_get.return_value.content = data

            df = fetch_data("https://localhost")
            self.assertEqual((30, 11), df.shape, "Shape should match")

    def test_get_region_data_filters_region(self) :
        region_data = get_region_data(self.region_df, ["01"])
        region_data = region_data["01"]

        self.assertEqual((7, 2), region_data.shape, "Returned shape should only contain one region")

        region_data = get_region_data(self.region_df, ["02"])
        region_data = region_data["02"]

        self.assertEqual((3, 2), region_data.shape, "Returned shape should only contain one region")

    def test_get_nation_data_gets_days(self) :
        nation_data = get_nation_data(self.nation_df)

        self.assertEqual((3, 2), nation_data.shape, "Returned shape should only contain one region")


