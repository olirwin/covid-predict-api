from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List

load_dotenv()

AVAILABLE_REGIONS = ["FRA", "59", "62"]


def check_dates_order(start_date : date, end_date : date) -> bool :
    return start_date <= end_date


def check_start_date(start_date : date) -> bool :
    return start_date >= date(2020, 6, 1)


def check_end_date(end_date : date) -> bool :
    max_days_ahead = int(os.getenv("MAX_DAYS_AHEAD", 90))
    return end_date <= date.today() + timedelta(days = max_days_ahead)


def check_predict_start(start_date : date) -> bool :
    max_days_behind = int(os.getenv("MAX_DAYS_BEHIND", 3))
    return start_date >= date.today() - timedelta(days = max_days_behind)


def check_region(region : str) -> bool :
    return region in AVAILABLE_REGIONS


def check_all(start_date : date,
              end_date : date,
              region : str,
              prediction : bool = False) -> List[InvalidParameter] :

    invalids : List[InvalidParameter] = []

    if not check_region(region) :
        invalids.append(InvalidParameter("region", f"Selected region {region} is not available"))

    if not check_start_date(start_date) :
        invalids.append(InvalidParameter("start_date", f"Start date is before 01/06/2020"))

    if not check_end_date(end_date) :
        invalids.append(InvalidParameter("end_date",
                                         f"End date is too late in the future, predictions would not be precise"))

    if not check_dates_order(start_date, end_date) :
        invalids.append(InvalidParameter("end_date", "End date is before start date"))

    if prediction and not check_predict_start(start_date) :
        max_days_behind = int(os.getenv("MAX_DAYS_BEHIND", 3))
        invalids.append(InvalidParameter("start_date",
                                         f"Start date cannot be before "
                                         f"{date.today() - timedelta(days = max_days_behind)}"))

    return invalids


@dataclass
class InvalidParameter :

    field : str
    message : str
