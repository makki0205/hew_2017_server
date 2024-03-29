#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
try:
    import thread
except ImportError:
    import _thread as thread #Py3K changed it.
from util.SocketManager import socketManager


HOST = '192.168.100.199'
PORT = 6666
BACKLOG = 10
BUFSIZE = 1024

class Socket():
    connect={}
    def __init__(self, host=HOST, port = PORT):
        # socketの作成
        # AF_INET : ipv4, SOCK_STREAM : TCP
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ソケットにローカルアドレスをバインド
        self.s.bind((host, port))
        # 接続
        self.s.listen(BACKLOG)
        thread.start_new_thread(self.run,())

    def sendAll(self, msg):
        # print (type(msg))
        msg = msg.encode('utf-8')
        for k, conn in self.connect.items():
            conn.send(msg)

    def run(self):
        while 1:
            conn, addr = self.s.accept()
            self.connect[addr[0]+str(addr[1])] = conn
            thread.start_new_thread(self.handler, (conn, addr))

    def handler(self,clientsock,addr):
        while 1:
            data = self.connect[addr[0]+str(addr[1])].recv(BUFSIZE)
            if not data:
                break
            msg = data.decode("utf-8")
            socketManager.send_index(msg)

        self.connect[addr[0]+str(addr[1])].close()
        del self.connect[addr[0]+str(addr[1])]
