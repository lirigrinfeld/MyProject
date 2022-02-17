import socket
import select


class Server:

    def __init__(self):
        ip = "0.0.0.0"
        port = 8835
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        print("Listening for clients...")

        self.client_sockets = []
        self.messages_to_send = []

    def receive_client_msg(self, client_socket):
        data = client_socket.recv(2)
        length = data.decode()
        command = client_socket.recv(int(length)).decode()
        return command

    def loop_body(self):
        rlist, wlist, xlist = select.select([self.server_socket] + self.client_sockets, self.client_sockets, [])
        for current_socket in rlist:
            if current_socket is self.server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                self.client_sockets.append(connection)
                connection.send("you are connected".encode())

            else:
                command = self.receive_client_msg(current_socket)
                print(f"command: {command}")
                if command.upper() == 'EXIT':
                    self.client_sockets.remove(current_socket)
                    print("Connection closed")
                    current_socket.close()
                else:
                    self.messages_to_send.append([current_socket, command])
                    for message in self.messages_to_send:
                        current_socket, data = message
                        if current_socket in wlist:
                            self.messages_to_send.remove(message)


def main():
    s = Server()
    while True:
        s.loop_body()


if __name__ == '__main__':
    main()
