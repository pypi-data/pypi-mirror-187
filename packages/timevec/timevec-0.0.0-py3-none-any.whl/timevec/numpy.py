import datetime

import numpy as np
import numpy.typing as npt


def year_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    begin_of_year = datetime.datetime.min.replace(year=dt.year)
    end_of_year = datetime.datetime.min.replace(year=dt.year + 1)
    year_seconds = (end_of_year - begin_of_year).total_seconds()
    seconds_since_begin_of_year = (dt - begin_of_year).total_seconds()
    rate = seconds_since_begin_of_year / year_seconds
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2 * np.pi * rate)
    vec[1] = np.sin(2 * np.pi * rate)
    return vec


def month_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
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
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2 * np.pi * rate)
    vec[1] = np.sin(2 * np.pi * rate)
    return vec


def week_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
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
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2 * np.pi * rate)
    vec[1] = np.sin(2 * np.pi * rate)
    return vec


def day_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
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
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2 * np.pi * rate)
    vec[1] = np.sin(2 * np.pi * rate)
    return vec
