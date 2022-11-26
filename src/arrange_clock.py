import obspython as obs
from datetime import datetime, timedelta
from typing import Optional
from logic import make_display_time, get_sorted_timezones, get_timeoffset_from_ntp, USE_PC_TIMEZONE
from osb_util import set_source_list

# constants
CLOCK_UPDATE_INTERVAL_MS = 50
NTP_REQUEST_INTERVAL_MS = 30 * 60 * 1000
NTP_HOST_UPDATE_WAIT_MS = 1 * 1000  # ntp server urlが変更されてもすぐにNTPサーバーに接続しないようにすることで変更途中のときに更新しないようにする。

# global variables
source_name = ""
clock_format_str = ""
ntp_server_host = ""
time_offset: Optional[timedelta] = timedelta(seconds=0)
timezone_name: Optional[str] = None


def script_properties():
    props = obs.obs_properties_create()
    source_list = obs.obs_properties_add_list(
        props, "source", "Display source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
    )

    time_zone_list = obs.obs_properties_add_list(
        props, "timezone_name", "Time zone", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING
    )

    set_source_list(source_list, {"text_gdiplus", "text_ft2_source"})

    for timezone in get_sorted_timezones():
        obs.obs_property_list_add_string(time_zone_list, timezone, timezone)

    obs.obs_properties_add_text(props, "clock_format_str", "Clock format", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "ntp_server_host", "NTP server url", obs.OBS_TEXT_DEFAULT)
    return props


def source_activated(cd):
    pass


def source_deactivated(cd):
    pass


def script_update(settings):
    global source_name, clock_format_str, ntp_server_host, timezone_name

    # get parameters from UI
    source_name = obs.obs_data_get_string(settings, "source")
    new_clock_format_str = obs.obs_data_get_string(settings, "clock_format_str")
    new_ntp_server_host = obs.obs_data_get_string(settings, "ntp_server_host")
    new_timezone_name = obs.obs_data_get_string(settings, "timezone_name")

    if new_clock_format_str != clock_format_str:
        clock_format_str = new_clock_format_str
        obs.timer_remove(timer_callback)
        obs.timer_add(timer_callback, CLOCK_UPDATE_INTERVAL_MS)

    if new_ntp_server_host != ntp_server_host:
        ntp_server_host = new_ntp_server_host
        obs.timer_remove(get_ntp_callback)
        obs.timer_add(get_ntp_callback, NTP_HOST_UPDATE_WAIT_MS)

    if new_timezone_name != timezone_name:
        timezone_name = new_timezone_name


def script_description():
    return "This script can show customizable clock on text source.\n\nMade by Nanahuse"


def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "timezone_name", USE_PC_TIMEZONE)
    obs.obs_data_set_default_string(settings, "clock_format_str", "%Y-%m-%d %H:%M:%S")
    obs.obs_data_set_default_string(settings, "ntp_server_host", "")


def script_load(settings):
    signal_handler = obs.obs_get_signal_handler()
    obs.signal_handler_connect(signal_handler, "source_activate", source_activated)
    obs.signal_handler_connect(signal_handler, "source_deactivate", source_deactivated)


def get_ntp_callback():
    global ntp_server_host, time_offset
    time_offset = get_timeoffset_from_ntp(ntp_server_host)

    obs.timer_remove(get_ntp_callback)
    obs.timer_add(get_ntp_callback, NTP_REQUEST_INTERVAL_MS)


def timer_callback():
    global source_name, clock_format_str, time_offset, timezone_name
    if source_name == "":
        return

    source = obs.obs_get_source_by_name(source_name)
    if source is None:
        return

    now_time_string = ""

    if time_offset is None:
        now_time_string = "[NTP Connection Error]"
    else:
        now_time = datetime.now() + time_offset
        now_time_string = make_display_time(now_time, timezone_name, clock_format_str)

    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", now_time_string)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)
