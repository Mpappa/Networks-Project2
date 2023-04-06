import socket
import threading

class User:
    def __init__(self, username, client):
        self.username = username
        self.client = client

class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 12345
        self.users = []
        self.messages = []
        
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server is running on {self.host}:{self.port}")

        while True:
            client, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, ))
            thread.start()
        
    def handle_client(self, client):
        username = client.recv(1024).decode()
        user = User(username, client)
        self.users.append(user)
        client.send(b"You have joined the group.")
        self.broadcast(f"{username} has joined the group.")
        self.display_users()
        self.display_messages(user)
        
        while True:
            try:
                message = client.recv(1024).decode()
                if message == "exit":
                    self.remove_user(user)
                    break
                self.messages.append((len(self.messages) + 1, username, message))
                self.broadcast(f"New message from {username}")
                self.display_messages(user)
            except:
                self.remove_user(user)
                break
                
    def remove_user(self, user):
        self.users.remove(user)
        user.client.send(b"You have left the group.")
        self.broadcast(f"{user.username} has left the group.")
        self.display_users()
        
    def display_users(self):
        users = "Users:\n"
        for user in self.users:
            users += f"- {user.username}\n"
        self.broadcast(users)

    def display_messages(self, user):
        messages = "Last 2 messages:\n"
        for message in self.messages[-2:]:
            messages += f"ID:{[i]}, - {message[0]}: {message[1]} - {message[2]}\n"
            i += 1
        user.client.send(messages.encode())

    def broadcast(self, message):
        for user in self.users:
            user.client.send(message.encode())

if __name__ == '__main__':
    server = Server()
    server.start()