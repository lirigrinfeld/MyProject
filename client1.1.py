import socket
import select

class Client:

    def __init__(self):
        ip = "127.0.0.1"
        port = 8835
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def send_msg_to_server(self, msg):
        message_length = str(len(msg))
        zfill_message_length = message_length.zfill(2)
        message = zfill_message_length + msg
        self.client_socket.send(message.encode())

    def body(self):
        msg = "ready"
        self.send_msg_to_server(msg)

        while True:
            rlist, wlist, xlist = select.select([self.client_socket], [], [], 0.01)
            for current_socket in rlist:
                #i am the current socket:
                data = current_socket.recv(1024)
                print(data.decode())

        if msg.upper() == 'EXIT':
            self.client_socket.close()


def main():
    c = Client()
    c.body()
    c.client_socket.close()


if __name__ == '__main__':
    main()