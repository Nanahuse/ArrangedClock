# Copyright (c) 2022 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ArrangedClock/blob/main/LICENSE

import zoneinfo
from datetime import datetime, timedelta
from ntplib import NTPClient
from typing import Optional

USE_PC_TIMEZONE = "use PC timezone"


def get_sorted_timezones() -> list[str]:
    raw_timezones = zoneinfo.available_timezones()
    major_timezones = sorted(
        [
            timezone
            for timezone in raw_timezones
            if "/" not in timezone and "GMT" not in timezone and not timezone.startswith("Etc")
        ]
    )

    def add_sign(x):
        return f"+{x}" if x > 0 else f"{x}"

    gmt_timezones = [f"Etc/GMT{add_sign(i)}" for i in range(-14, 13)]

    region_timezone = sorted(
        [timezone for timezone in raw_timezones if "/" in timezone and not timezone.startswith("Etc")]
    )

    return [USE_PC_TIMEZONE] + major_timezones + gmt_timezones + region_timezone


def make_display_time(raw_time: datetime, timezone_name: str, string_format) -> str:
    try:
        if timezone_name == "":
            raise zoneinfo.ZoneInfoNotFoundError(timezone_name)

        if timezone_name == USE_PC_TIMEZONE:
            converted_time = raw_time.astimezone(tz=None)
        else:
            converted_time = raw_time.astimezone(tz=zoneinfo.ZoneInfo(timezone_name))
        return converted_time.strftime(string_format)

    except zoneinfo.ZoneInfoNotFoundError as e:
        print(e)
        return "[Time zone] is invalid"
    except ValueError as e:
        print(e)
        return "[clock format str] is invalid"
    except Exception as e:
        print(e)
        return "[Unexpected Error]"


def get_timeoffset_from_ntp(ntp_host: str) -> Optional[timedelta]:
    try:
        if ntp_host == "":
            return timedelta()
        ntp_client = NTPClient()
        res = ntp_client.request(ntp_host)
        return timedelta(seconds=res.offset)
    except Exception as e:
        print(e)
        return None
