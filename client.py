# -*- coding:utf-8 -*-
import socket
import json
try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.

host = "localhost" #お使いのサーバーのホスト名を入れます
port = 6666 #適当なPORTを指定してあげます

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします

client.connect((host, port)) #これでサーバーに接続します

msg = {
    "hit":True
}
client.send(json.dumps(msg).encode("utf-8")) #適当なデータを送信します（届く側にわかるように）
