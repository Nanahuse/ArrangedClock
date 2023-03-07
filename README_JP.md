[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[*ENGLISH PAGE*](README.md)

# ArrangedClock
OBSのテキストソースにカスタマイズ可能な時計を表示できます。

* 時計表記を指定できる。
* タイムゾーンの指定ができる
* NTPにより正確な時刻を表示できる

*このスクリプトを使うためにはOBS28とPython 3.10以降が必要になります*


# Setup
**[導入の説明(note)](https://note.com/nanahuse/n/ndb2f96beba76)**

1. [リリースページ](https://github.com/Nanahuse/ArrangedClock/releases)から最新のバージョンのZIPファイルをダウンロードする.
2. [requirements.txt](requirements.txt)を使った依存ライブラリのインストール<br>```$ pip install -r requirements.txt```
3. OBS -> ツール -> スクリプト -> Pythonの設定<br>Pythonインストールパスを設定する ※Python 3.10 or laterが必須。
4. OBS -> ツール -> スクリプト<br>＋ボタンからスクリプトの追加を行う。 arrange_clock.pyを選択する。

# How to use
## Display source
時計を表示するテキストソースを選ぶ
## Time zone
時計のタイムゾーンの指定

## Clock format
時計の書式はPython datetime strftimeを使用します。<br>
こちらのドキュメントを参考にしてください -> [Python datetime document](https://docs.python.org/ja/3.10/library/datetime.html#strftime-and-strptime-format-codes)<br>
※いくつか追加の表示書式にも対応しています。（下記参照）

### カスタム書式
Directive|Meaning|Example
:-|:-|:-
%nm|月を表す数字（0埋めなし）| 1, 2, ..., 12
%nd|日を表す数字（0埋めなし） | 1, 2, ..., 31

### Sample
```%Y-%m-%d %A %H:%M:%S``` -> 2021-10-18 Monday 21:00:00<br>
```%Y-%m-%d %A %H:%M``` -> 2021/10/18 Mon. 21:00<br>
```%Y-%nm-%nd``` -> 2021/1/1

## NTP server url
補正のために使用するNTPサーバーのURLを指定する。<br>*空欄にするとNTPによる補正を使用しない*


