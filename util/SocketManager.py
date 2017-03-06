
class SocketManager(object):
    index_Socket = []
    def set_index(self, conn):
        self.index_Socket.append(conn)

    def get_index(self):
        return self.index_Socket

    def delete_index(self, conn):
        self.index_Socket.remove(conn)

    def send_index(self, msg):
        for conn in self.index_Socket:
            conn.write_message(msg)

socketManager = SocketManager()
