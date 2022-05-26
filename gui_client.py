from tkinter import*
import socket
import protocol
from tkinter import filedialog as fd
import tkinter as tk


class Gui_Panel():
    def __init__(self, pHandler):
        self.top = tk.Tk()
        self.pHandler = pHandler
        self.file_name = None

    def gui_buttons(self):
        b1 = tk.Button(self.top, text='Load Scene', width=25, height=5, command=self.load_scene)
        b1.pack()
        b2 = tk.Button(self.top, text='Stop', width=25, height=5, command=self.stop)
        b2.pack()
        b3 = tk.Button(self.top, text='Start', width=25, height=5, command=self.start)
        b3.pack()
        b4 = tk.Button(self.top, text='Animation', width=25, height=5, command=self.animation)
        b4.pack()
        self.top.mainloop()

    def load_scene(self):
        file_path = fd.askopenfilename()
        self.file_name = file_path.split('/')[-1]
        self.pHandler.send_msg_to_server(f"command info load scene:{self.file_name}")

    def stop(self):
        self.pHandler.send_msg_to_server("command info stop")

    def start(self):
        self.pHandler.send_msg_to_server("command info start")

    def animation(self):
        top = Toplevel(self.top)
        tl = top_level(top, self.pHandler)
        tl.buttons()


class top_level():
    def __init__(self, top, pHandeler):
        self.top = top
        self.pHandler = pHandeler
        self.b1 = None
        self.steps = None
        self.iterations = None

    def buttons(self):
        tk.Label(self.top, text='Steps').place(x=30, y=50)
        tk.Label(self.top, text='Iterations').place(x=30, y=80)
        self.steps = tk.Entry(self.top)
        self.steps.place(x=90, y=50)
        self.iterations = tk.Entry(self.top)
        self.iterations.place(x=90, y=80)
        self.b1 = tk.Button(self.top, text='submit', command=self.update_scene)
        self.b1.place(x=100, y=110)

    def update_scene(self):
        self.pHandler.send_msg_to_server(f"command info animation {self.steps.get()} {self.iterations.get()}")
        print(self.steps.get(), self.iterations.get())
        self.top.destroy()


class App_Network:
    def __init__(self):
        ip = "127.0.0.1"

        port = 8830
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))


class Gui_Client:
    def __init__(self, pHandler):
        self.panel = Gui_Panel(pHandler)
        self.panel.gui_buttons()
        # self.panel.top.mainloop()

    def loop(self):
        # rlist, wlist, xlist = select.select([self.client_socket], [], [], 0.01)
        # for current_socket in rlist:
            # i am the current socket:
            # data = current_socket.recv(1024)
            # print(data.decode())
            # if button_press:
            #     protocol.send_msg_to_server(f"command info {self.panel.get_button()}", self.client_socket)
        pass


if __name__ == '__main__':
    my_net = App_Network()
    handler = protocol.ProtocolHandler(my_net.client_socket)
    c = Gui_Client(handler)
