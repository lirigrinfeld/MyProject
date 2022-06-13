import socket
import select
import pickle

import protocol
import Module

import tkinter
from tkinter import Tk, Canvas, Frame, BOTH, Toplevel


import pyautogui


class GuiScreen:
    def __init__(self, tk, res_x, res_y, pos_x, pos_y):
        super().__init__()
        self.root = tk
        self.canvas = None
        self.initUI(res_x, res_y, pos_x, pos_y)

    def initUI(self, res_x, res_y, pos_x, pos_y):
        self.root.geometry(f"{res_x}x{res_y}+{pos_x}+{pos_y}")
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill=BOTH, expand=1)

    def clear(self):
        if self.canvas is not None:
            self.canvas.delete("all")

    def draw(self, scene):
        self.clear()
        scene.draw(self.canvas)


class Client:

    def __init__(self, root):
        ip = "127.0.0.1"

        port = 8830
        self.tk = root
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))

        self.pHandler = protocol.ProtocolHandler(self.client_socket)

        self.num = None
        self.pHandler.send_msg_to_server(f"ready to present")
        msg = self.pHandler.get_msg_from_server()
        if "ID" in msg:
            self.num = msg.replace("ID", "")
        print(f"My ID: {self.num}")

        self.scene = None

        self.gui_screen = GuiScreen(self.tk, 500, 500, 0, 0)

    def get_binary_msg_from_server(self):
        msg_length = self.client_socket.recv(6)
        msg_length = int(msg_length.decode())
        binary_msg = self.client_socket.recv(msg_length)
        while len(binary_msg) < msg_length:
            binary_msg += self.client_socket.recv(msg_length-len(binary_msg))
        return binary_msg

    def iteration_body(self):
        rlist, wlist, xlist = select.select([self.client_socket], [], [], 0.01)
        for current_socket in rlist:
            # I am the current socket:
            # data = current_socket.recv(1024)
            # print(data.decode())
            self.scene = pickle.loads(self.get_binary_msg_from_server())
            print(self.scene)
            self.gui_screen.draw(self.scene)

            self.pHandler.send_msg_to_server(str(self.num))

        rlist == None

        self.tk.after(40, self.iteration_body)

    # def body(self):
    #     while True:
    #         rlist, wlist, xlist = select.select([self.client_socket], [], [], 0.01)
    #         for current_socket in rlist:
    #             self.scene = pickle.loads(self.get_binary_msg_from_server())
    #             print(self.scene)
    #             self.draw_screen()
    #
    #         rlist == None
    #
    #     if msg.upper() == 'EXIT':
    #         self.client_socket.close()


def main():
    root = Tk()

    c = Client(root)
    root.after(40, c.iteration_body)

    root.mainloop()

    c.client_socket.close()


if __name__ == '__main__':
    main()