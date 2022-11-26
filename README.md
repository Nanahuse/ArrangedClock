[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[*日本語の説明はこちら*](README_JP.md)


# ArrangeClock
This script can show customizable clock on text source.

* Customizable clock string
* Time Zone select
* NTP adjust

*This script only works on OBS28 and Python 3.10 or later*


# Setup
1. Download latest version from ReleasePage.
2. Install dependent library by [requirements.txt](requirements.txt)<br>```$ pip install -r requirements.txt```
3. OBS -> tool -> script -> Python Settings<br>Set python.exe path (Python 3.10 or later)
4. OBS -> tool -> script<br>add script (select -> arrange_clock.py)

# How to use
## Display source
select text source

## Time zone
You can display other countries clock.

## Clock format
```%Y-%m-%d %A %H:%M:%S``` -> 2021-10-18 Monday 21:00:00<br>
```%Y-%m-%d %A %H:%M``` -> 2021/10/18 Mon. 21:00

Clock format follows Python datetime strftime.<br>
Please refer to [Python datetime document](https://docs.python.org/3.10/library/datetime.html#strftime-and-strptime-format-code)


## NTP server url
*if blank, NOT adjust by NTP (use your own PC clock)*


## Attention
*This script only works on OBS28 and Python 3.10 or later*