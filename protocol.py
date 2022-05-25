
class ProtocolHandler:
    def __init__(self, connect_socket):
        self.socket = connect_socket

    def receive_client_msg(self):
        data = self.socket.recv(6)
        length = data.decode()
        command = self.socket.recv(int(length)).decode()
        return command
        # command = "initial_connection <id>"
        # command = "ready_to_present"


    def send_msg_to_client(self, msg):
        self.socket.send(str(len(msg)).zfill(6).encode())
        self.socket.send(msg.encode())


    def send_msg_to_server(self, msg):
        message_length = str(len(msg))
        zfill_message_length = message_length.zfill(6)
        message = zfill_message_length + msg
        self.socket.send(message.encode())


    def get_msg_from_server(self):
        msg_length = self.socket.recv(6)
        msg_length = int(msg_length.decode())
        msg = self.socket.recv(msg_length).decode()
        while len(msg) < msg_length:
            msg += self.socket.recv(msg_length-len(msg)).decode()
        print(f"msg_length: {msg_length}. msg: {msg}")
        return msg
