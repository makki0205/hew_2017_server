# -*- coding:utf-8 -*-
import socket
import json
try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.
import time

host = "192.168.100.199" #お使いのサーバーのホスト名を入れます
port = 6666 #適当なPORTを指定してあげます

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします

client.connect((host, port)) #これでサーバーに接続します

msg = {
    "hit":False
}
ohmsg = {
    "hit":True
}
client.send(json.dumps(msg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
time.sleep(2)
client.send(json.dumps(msg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
time.sleep(2)
client.send(json.dumps(ohmsg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
time.sleep(2)
client.send(json.dumps(msg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
time.sleep(2)
client.send(json.dumps(msg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
time.sleep(2)

client.send(json.dumps(ohmsg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
time.sleep(2)
