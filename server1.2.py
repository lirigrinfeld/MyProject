import pickle_try
import recangle
import socket
import select
import pyautogui
import protocol


class BBox:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy

    def __str__(self):
        return f"[{self.minx}, {self.miny}, {self.maxx}, {self.maxy}]"


class Server:
    command = None
    i = 1
    width, height = pyautogui.size()
    file_name = None

    def __init__(self):
        ip = "0.0.0.0"
        port = 8830
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        print("Listening for clients...")

        self.client_sockets = []
        self.messages_to_send = []
        self.bbox_dict = {}

        # file_name = "important.liri"
        # self.file_handler = pickle_try.LirisFileHandler(file_name)

        self.screens = {}

    def send_binary_msg_to_client(self, binary_msg, client_socket):
        client_socket.send(str(len(binary_msg)).zfill(6).encode())
        client_socket.send(binary_msg)

    def find_key(self, val):
        for key, value in self.screens.items():
            if val == value:
                return key
            return None

    def set_boundaries(self, str_val):
        val = int(str_val)
        return BBox((val-1)*Server.width, 0, (val*Server.width)-1, Server.height-1)

    def loop_body(self):
        rlist, wlist, xlist = select.select([self.server_socket] + self.client_sockets, [], [])
        for current_socket in rlist:
            if current_socket is self.server_socket:
                connection, client_address = current_socket.accept()
                print(f"New client joined! ", connection)
                self.client_sockets.append(connection)
                # connection.send("you are connected".encode())
            else:
                # (object)
                pHandler = protocol.ProtocolHandler(current_socket)
                msg = pHandler.receive_client_msg()
                print(f"msg: '{msg}'")
                # if initial_connation...
                num = None
                num_of_steps = 0
                if "initial info" in msg:
                    num = msg.replace("initial info ", "")
                    if current_socket not in self.screens:
                        self.screens[current_socket] = num
                    print(self.screens)
                    print(self.set_boundaries(self.screens[current_socket]))
                elif "command info " in msg:
                    msg = msg.replace("command info ", "")
                    if "load scene" in msg:
                        Server.file_name = msg.split(':')[1]
                    elif "start" in msg or "stop" in msg:
                        Server.command = msg
                    elif "animation" in msg:
                        num_of_steps = int(msg.replace("animation ", ""))
                    print(f"Server.command: {Server.command}")
                    print(f"Server.file_name: {Server.file_name}")

                # if ready_to_present ...
                if Server.file_name is not None:
                    # if self.screens is not [] and Server.command == "start" and Server.file_name is not None:
                    for s in self.client_sockets:
                        if s in self.screens:
                            file_handler = pickle_try.LirisFileHandler(Server.file_name)
                            # לקבל גם מספר ולפי המספר לחשב לו את הגבולות
                            scene = file_handler.read_from_file()
                            recangle.Scene.shift(scene, num_of_steps)
                            if self.screens is not [] and Server.command == "start":
                                BLoB = file_handler.serialize_to_object(scene.bbox_scene(self.set_boundaries(self.screens[s])))
                                self.send_binary_msg_to_client(BLoB, s)


def main():
    s = Server()
    while True:
        s.loop_body()


if __name__ == '__main__':
    main()
