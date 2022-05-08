import pickle_try
import recangle
import socket
import select
import pyautogui


class BBox:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def __str__(self):
        return f"[{self.minx}, {self.miny}, {self.maxx}, {self.maxy}]"


class Server:
    i = 1
    def __init__(self):
        ip = "0.0.0.0"
        port = 8835
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        print("Listening for clients...")

        self.client_sockets = []
        self.messages_to_send = []
        self.bbox_dict = {}

        file_name = "important.liri"
        self.file_handler = pickle_try.LirisFileHandler(file_name)

        self.screens = {}

    def receive_client_msg(self, client_socket):
        data = client_socket.recv(6)
        length = data.decode()
        command = client_socket.recv(int(length)).decode()
        return command

    def send_msg_to_client(self, msg, client_socket):
        client_socket.send(str(len(msg)).zfill(6).encode())
        client_socket.send(msg.encode())

    def send_binary_msg_to_client(self, binary_msg, client_socket):
        client_socket.send(str(len(binary_msg)).zfill(6).encode())
        client_socket.send(binary_msg)

    def find_key(self, val):
        for key, value in self.bbox_dict.items():
            if val == value:
                return key
            return None

    def set_boundaries(self, val):
        client_socket = self.find_key(val)
        width = self.receive_client_msg(client_socket)
        height = self.receive_client_msg(client_socket)
        return (val-1)*width+1, 0, val*width, height

    def loop_body(self):
        rlist, wlist, xlist = select.select([self.server_socket] + self.client_sockets, [], [])
        for current_socket in rlist:
            if current_socket is self.server_socket:
                connection, client_address = current_socket.accept()
                print(f"New client joined! ", connection)
                self.client_sockets.append(connection)
                self.screens[connection] = self.receive_client_msg(connection)
                print(self.screens)
                # connection.send("you are connected".encode())
            else:
                # (object)
                current_socket.recv(1024)
                print(self.set_boundaries(1))
                # לקבל גם מספר ולפי המספר לחשב לו את הגבולות
                BLoB = self.file_handler.serialize_to_object(self.file_handler.read_from_file())
                self.send_binary_msg_to_client(BLoB, current_socket)
def main():
    s = Server()

    while True:
        s.loop_body()


if __name__ == '__main__':
    main()
