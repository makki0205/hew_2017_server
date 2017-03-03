#-*- coding:utf-8 -*-
import os
import random
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from util.Socket import Socket

socket = Socket()
source_str = 'abcdefghijklmnopqrstuvwxyz0123456789'
current_key = ""
cl=[]
BASE_DIR = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global current_key
        current_key = "".join([random.choice(source_str) for x in range(30)])
        print(current_key)
        self.render("index.html",hash=current_key)

class Gun(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument("key") == current_key:
            self.render("app.html")
        else:
            self.write("404")
#クライアントからメッセージを受けるとopen → on_message → on_closeが起動する
class AppSocketHandler(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        try:
            data = json.loads(message)
            if data['key'] == current_key:
                data.pop('key')
                print(data)
                socket.sendAll(json.dumps(data))
        except Exception as e:
            pass

    def check_origin(self, origin):
        return True

class RaspySocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ("open")
        if self not in cl:
            cl.append(self)

    #websockeクローズ
    def on_close(self):
        print ("close")
        if self in cl:
            cl.remove(self)

# settings = {
#     "static_path": os.path.join(os.path.dirname(__file__), "public"),
# }
app = tornado.web.Application([
    (r"/websocket", AppSocketHandler),
    (r"/raspy", RaspySocketHandler),
    (r"/app", Gun),
    (r"/", MainHandler)
],static_path=os.path.join(BASE_DIR, 'static'),
)

if __name__ == "__main__":
   app.listen(8000)
   tornado.ioloop.IOLoop.instance().start()
