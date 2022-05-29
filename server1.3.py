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
    state = None
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

        self.active_scene = None

        self.file_handler = None

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

    def scene_export(self):
        for s in self.client_sockets:
            if s in self.screens:
                pHandler = protocol.ProtocolHandler(s)
                print(f"handling screen: {s}")
                sub_scene = recangle.Scene.bbox_scene(self.active_scene, self.set_boundaries(self.screens[s]))
                print(f"current sub scene = {sub_scene}")
                pHandler.send_msg_to_client("starting the scene export")
                contents = []
                for r in sub_scene.rectangles:
                    if (r.content != "None") and (r.content not in contents):
                        contents.append(r.content)
                print(f"contents: {contents}")
                pHandler.send_msg_to_client(str(len(contents)))
                for c in contents:
                    print(f"pHandler.send_msg_to_client(c): {pHandler.send_msg_to_client(c)}")
                    pHandler.send_msg_to_client(c)
                    self.send_file(pHandler.socket, c)
                BLoB = self.file_handler.serialize_to_object(sub_scene)
                self.send_binary_msg_to_client(BLoB, s)

    def send_file(self, client_socket, image_path):
        image_file = open(image_path, 'rb')
        image_binary = image_file.read(999999)
        print(f"1: the length of image binary: {len(image_binary)}")
        while len(image_binary) > 0:
            self.send_binary_msg_to_client(image_binary, client_socket)
            image_binary = image_file.read(999999)
            print(f"2: the length of image binary: {len(image_binary)}")
        image_file.close()
        print(f"file closed!! sending '0' to client")
        client_socket.send("0".zfill(6).encode())

    # def clear(self):
    #     empty_scene = recangle.Scene([])
    #     self.scene_export(empty_scene)

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
                # if initial_connection...
                # num = None
                # num_of_steps = 0
                if "ready to present" in msg:
                    num = Server.i
                    Server.i += 1
                    if current_socket not in self.screens:
                        self.screens[current_socket] = num
                        if self.active_scene is not None:
                            self.active_scene.update_width(Server.width * len(self.screens))
                        pHandler.send_msg_to_client(f"ID{num}")
                    print(self.screens)
                    print(self.set_boundaries(self.screens[current_socket]))
                elif "command info " in msg:
                    msg = msg.replace("command info ", "")
                    if "load scene" in msg:
                        Server.file_name = msg.split(':')[1]
                        self.file_handler = pickle_try.LirisFileHandler(Server.file_name)
                        # לקבל גם מספר ולפי המספר לחשב לו את הגבולות
                        self.active_scene = self.file_handler.read_from_file()
                        self.active_scene.update_width(Server.width * len(self.screens))
                    elif "start" in msg or "stop" in msg:
                        Server.state = msg
                        if (Server.file_name is not None) and (len(self.screens) != 0) and (Server.state == "start"):
                            self.scene_export()
                        elif Server.file_name is None:
                            print("You need to load a scene before you start one...")
                        elif len(self.screens) == 0:
                            print("You need to open a client before you start one...")
                    elif "animation" in msg:
                        steps_and_iterations = msg.replace("animation ", "").split()
                        num_of_steps = int(steps_and_iterations[0])
                        num_of_iterations = int(steps_and_iterations[1])
                        if Server.file_name is not None:
                            for i in range(num_of_iterations):
                                recangle.Scene.shift(self.active_scene, num_of_steps, Server.width*len(self.screens))
                                if Server.state == "start":
                                    self.scene_export()
                        elif Server.file_name is None:
                            print("You need to load a scene before you edit one...")
                    print(f"Server.command: {Server.state}")
                    print(f"Server.file_name: {Server.file_name}")

                # # if ready_to_present ...
                # if Server.file_name is not None:
                #     # if self.screens is not [] and Server.command == "start" and Server.file_name is not None:
                #     for s in self.client_sockets:
                #         if s in self.screens:
                #             file_handler = pickle_try.LirisFileHandler(Server.file_name)
                #             # לקבל גם מספר ולפי המספר לחשב לו את הגבולות
                #             self.active_scene = file_handler.read_from_file()
                #             recangle.Scene.shift(self.active_scene, num_of_steps)
                #             if self.screens is not [] and Server.command == "start":
                #                 BLoB = file_handler.serialize_to_object(self.active_scene.bbox_scene(self.set_boundaries(self.screens[s])))
                #                 self.send_binary_msg_to_client(BLoB, s)


def main():
    s = Server()
    while True:
        s.loop_body()


if __name__ == '__main__':
    main()
