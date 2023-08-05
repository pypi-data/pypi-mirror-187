import datetime
import math
from typing import Tuple


def year_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the year as a vector"""
    begin_of_year = datetime.datetime.min.replace(year=dt.year)
    end_of_year = datetime.datetime.min.replace(year=dt.year + 1)
    year_seconds = (end_of_year - begin_of_year).total_seconds()
    seconds_since_begin_of_year = (dt - begin_of_year).total_seconds()
    rate = seconds_since_begin_of_year / year_seconds
    x = math.cos(2 * math.pi * rate)
    y = math.sin(2 * math.pi * rate)
    return x, y


def month_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the month as a vector"""
    begin_of_month = datetime.datetime.min.replace(
        year=dt.year, month=dt.month
    )
    end_of_month = datetime.datetime.min.replace(
        year=dt.year, month=dt.month + 1
    )
    month_seconds = (end_of_month - begin_of_month).total_seconds()
    seconds_since_begin_of_month = (dt - begin_of_month).total_seconds()
    rate = seconds_since_begin_of_month / month_seconds
    x = math.cos(2 * math.pi * rate)
    y = math.sin(2 * math.pi * rate)
    return x, y


def week_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the week as a vector"""
    # weekday is 0 for Monday and 6 for Sunday
    current_time = (
        dt.weekday() * 24 * 60 * 60
        + dt.hour * 60 * 60
        + dt.minute * 60
        + dt.second
    )
    dow_all_time = 7 * 24 * 60 * 60
    rate = current_time / dow_all_time
    x = math.cos(2 * math.pi * rate)
    y = math.sin(2 * math.pi * rate)
    return x, y


def day_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the day as a vector"""
    begin_of_day = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=dt.day
    )
    end_of_day = datetime.datetime.min.replace(
        year=dt.year, month=dt.month, day=dt.day + 1
    )
    day_seconds = (end_of_day - begin_of_day).total_seconds()
    seconds_since_begin_of_day = (dt - begin_of_day).total_seconds()
    rate = seconds_since_begin_of_day / day_seconds
    x = math.cos(2 * math.pi * rate)
    y = math.sin(2 * math.pi * rate)
    return x, y
