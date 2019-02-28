#!/usr/bin/env python
# coding: UTF-8

#################################################################
# Copyright (C) 2017 Mono Wireless Inc. All Rights Reserved.    #
# Released under MW-SLA-*J,*E (MONO WIRELESS SOFTWARE LICENSE   #
# AGREEMENT).                                                   #
#################################################################

import uptime
import netifaces
import requests
from optparse import *
import datetime
import time
import threading
import os
import sys
import logzero
# WONO WIRELESSのシリアル電文パーサなどのAPIのインポート
sys.path.append('./MNLib/')
from apppal import AppPAL

# ライブラリのインポート


# ここより下はグローバル変数の宣言
# コマンドラインオプションで使用する変数
options = None
args = None

# 各種フラグ
bEnableErrMsg = False

# プログラムバージョン
Ver = "0.0.1"
userPath = 'user.txt'
tempPath = 'sensor.json'
user = ""

def ParseArgs():
    global options, args

    parser = OptionParser()
    if os.name == 'nt':
        parser.add_option('-t', '--target', type='string',
                          help='target for connection', dest='target', default='COM3')
    else:
        parser.add_option('-t', '--target', type='string',
                          help='target for connection', dest='target', default='/dev/ttyUSB_TWELite')

    parser.add_option('-b', '--baud', dest='baud', type='int',
                      help='baud rate for serial connection.', metavar='BAUD', default=115200)
    parser.add_option('-s', '--serialmode', dest='format', type='string',
                      help='serial data format type. (Ascii or Binary)',  default='Ascii')
    parser.add_option('-e', '--errormessage', dest='err',
                      action='store_true', help='output error message.', default=False)
    (options, args) = parser.parse_args()


if __name__ == '__main__':
    print("*** MONOWIRELESS App_PAL_Viewer " + Ver + " ***")

    ParseArgs()

    bEnableErrMsg = options.err
    try:
        PAL = AppPAL(port=options.target, baud=options.baud,
                     tout=0.05, sformat=options.format, err=bEnableErrMsg)
    except:
        print("Cannot open \"AppPAL\" class...")
        exit(1)

    interfaces = netifaces.interfaces()
    addrslist = []
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        addrslist.append(addrs[netifaces.AF_LINK][0]["addr"])
    
    try:
        with open(userPath) as f:
            user = f.read()
    except:
        print("Cannot open User File")

    logger = logzero.setup_logger(
        name='countIoT',      # loggerの名前、複数loggerを用意するときに区別できる
        logfile='sensor.log',       # ログファイルの格納先
        level=10,                   # 標準出力のログレベル
        formatter=None,             # ログのフォーマット
        maxBytes=10000000,              # ログローテーションする際のファイルの最大バイト数
        backupCount=5,              # ログローテーションする際のバックアップ数
        fileLoglevel=10,            # ログファイルのログレベル
        disableStderrLogger=False   # 標準出力するかどうか
    )

    while True:
        try:
            # データがあるかどうかの確認
            if PAL.ReadSensorData():
                # あったら辞書を取得する
                Data = PAL.GetDataDict()
                try:
                    Data["version"] = Ver
                    Data["macAddress"] = addrslist
                    Data["uptime"] = uptime.uptime()
                    headers = {'user': user}
                    response = requests.post(
                        'http://cloud.nefry.studio:1880/nefrysetting/sensorData', data=Data,headers=headers)
                    print(response.status_code)    # HTTPのステータスコード取得
                    print(response.text)    # レスポンスのHTMLを文字列で取得
                    
                except Exception as ex:
                    print(str(ex))
                    logger.debug(Data)

            # if os.path.isfile(tempPath):
            #     try:
            #         with open(tempPath) as f:
            #             try:
            #                 for s_line in f:
            #                     print(s_line)
            #                     headers = {'user': user}
            #                     response = requests.post(
            #                         'http://cloud.nefry.studio:1880/nefrysetting/sensorData', data=Data,headers=headers)
            #                     print(response.status_code)    # HTTPのステータスコード取得
            #                     print(response.text)    # レスポンスのHTMLを文字列で取得
            #                 os.remove(tempPath)
            #             except Exception as ex:
            #                 print(str(ex))

            #     except Exception as ex:
            #         print(str(ex))
            #         print("Cannot open User File")
        # Ctrl+C でこのスクリプトを抜ける
        except KeyboardInterrupt:
            break

    del PAL

    print("*** Exit App_PAL Viewer ***")
