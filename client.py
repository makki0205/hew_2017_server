#-*- coding:utf-8 -*-

from websocket import create_connection
import sys

#コネクションを張る
ws = create_connection("ws://makki0250.com:8000/raspy")

#メッセージを送信
# ws.send('hello world!')

#受信したメッセージを表示
while True:
    print (ws.recv())

#コネクションを切断
ws.close()
