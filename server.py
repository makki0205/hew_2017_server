#-*- coding:utf-8 -*-
import os
import random
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time
import datetime
from util.Socket import Socket
from util.SocketManager import socketManager

socket = Socket()
source_str = 'abcdefghijklmnopqrstuvwxyz0123456789'
current_key = ""
current_face = "default.jpg"
cl=[]
BASE_DIR = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global current_key
        current_key = "".join([random.choice(source_str) for x in range(30)])
        print(current_key)
        socket.sendAll(json.dumps({"set_state":0}))
        self.render("index.html",hash=current_key)

class Gun(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument("key") == current_key:
            self.render("app.html")
        else:
            self.write("404")

class Image(tornado.web.RequestHandler):

    def post(self):
        files = self.request.files
        file = files['upload_file'][0]['body']
        today = datetime.datetime.today()
        today = today.strftime('%Y%m%d%H%M%S')
        f = open('./static/face/' + today + '.jpg', 'wb')
        f.write(file)
        f.close()
        current_face = today + '.jpg'
        self.write("")
#クライアントからメッセージを受けるとopen → on_message → on_closeが起動する
class AppSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self not in cl:
            cl.append(self)

    #websockeクローズ
    def on_close(self):
        print ("close")
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
        try:
            data = json.loads(message)
            print(data)
            if data['key'] == current_key:
                if data['state'] == 0:
                    socket.sendAll(json.dumps({"set_state":0})) #TODO 変更
                    socketManager.send_index(json.dumps({"state":0}))
                elif data['state'] == 2:
                    socket.sendAll(json.dumps({"set_state":2})) #TODO 変更

                else:
                    data.pop('key')
                    print(data)
                    socket.sendAll(json.dumps(data))
            else:
                self.write_message(current_key)
        except Exception as e:
            pass

    def check_origin(self, origin):
        return True

class indexSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self not in socketManager.get_index():
            socketManager.set_index(self)

    #websockeクローズ
    def on_close(self):
        print ("close")
        if self in socketManager.get_index():
            socketManager.delete_index(self)

    def check_origin(self, origin):
        return True

# settings = {
#     "static_path": os.path.join(os.path.dirname(__file__), "public"),
# }
app = tornado.web.Application([
    (r"/websocket", AppSocketHandler),
    (r"/index", indexSocketHandler),
    (r"/image", Image),
    (r"/app", Gun),
    (r"/", MainHandler)
],static_path=os.path.join(BASE_DIR, 'static'),
)

if __name__ == "__main__":
   app.listen(8000)
   tornado.ioloop.IOLoop.instance().start()
