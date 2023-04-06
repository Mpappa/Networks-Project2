import socket
import threading

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def start(self):
        username = input("Enter a username: ")
        self.client_socket.send(username.encode())
        print(self.client_socket.recv(1024).decode())

        while True:
            message = input()
            self.client_socket.send(message.encode())
            if message == "exit":
                break
            print(self.client_socket.recv(1024).decode())
                
if __name__ == '__main__':
    client = Client()
    client.start()
