import socket
from main import *

server = "localhost"
port = 8080

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server, port))

room = input("Room: ")
mode = input("Mode: ")

if mode == "W":
    client_socket.send(b"W")
    sender = input("Sender: ")
    message = input("Message: ")

    data = room + "\n" + sender + "\n" + message

    send_message(client_socket, data)
if mode == "R":
    client_socket.send(b"R")
    n = int(input("How many messages would you like to receive: "))
    data = room + "\n" + str(n)
    send_message(client_socket, data)
    messages = receive_message(client_socket)
    print(messages)

client_socket.close()