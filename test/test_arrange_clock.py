# Copyright (c) 2022 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ArrangedClock/blob/main/LICENSE

import zoneinfo
from datetime import datetime
from logic import make_display_time, strftime, get_sorted_timezones, get_timeoffset_from_ntp, USE_PC_TIMEZONE


def test_make_display_time():
    assert (
        make_display_time(datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "UTC", "%Y/%m/%d %H:%M:%S")
        == "2000/01/01 11:11:11"
    )
    assert (
        make_display_time(
            datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "Asia/Tokyo", "%Y/%m/%d %H:%M:%S"
        )
        == "2000/01/01 20:11:11"
    )
    assert (
        make_display_time(
            datetime(2039, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "Asia/Tokyo", "%Y/%m/%d %H:%M:%S"
        )
        == "2039/01/01 20:11:11"
    )
    assert (
        make_display_time(
            datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "hogehoge", "%Y/%m/%d %H:%M:%S"
        )
        == "[Time zone] is invalid"
    )
    assert (
        make_display_time(datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "", "%Y/%m/%d %H:%M:%S")
        == "[Time zone] is invalid"
    )

    assert (
        make_display_time(datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "Asia/Tokyo", "%")
        == "[clock format str] is invalid"
    )
    assert make_display_time(datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "Asia/Tokyo", "") == ""
    assert (
        make_display_time(datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "Asia/Tokyo", "AA") == "AA"
    )

    assert make_display_time(1, "Asia/Tokyo", "") == "[Unexpected Error]"


def test_get_sorted_timezones():
    raw_timezones = zoneinfo.available_timezones()
    timezones = get_sorted_timezones()
    assert timezones[0] == USE_PC_TIMEZONE
    for timezone_name in timezones[1:]:
        assert timezone_name in raw_timezones


def test_get_timeoffset_from_ntp():
    assert get_timeoffset_from_ntp("ntp.nict.jp") is not None
    assert get_timeoffset_from_ntp("ntp.nict.j") is None


def test_strftime():
    assert strftime(datetime(2000, 1, 1, 11, 11, 11, tzinfo=zoneinfo.ZoneInfo("UTC")), "%Y-%nm-%nd") == "2000-1-1"
