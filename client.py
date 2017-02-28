#-*- coding:utf-8 -*-

from websocket import create_connection
import sys

#コネクションを張る
ws = create_connection("ws://localhost:8000/ws")

#メッセージを送信
ws.send('hello world!')

#受信したメッセージを表示
print (ws.recv())

#コネクションを切断
ws.close()
