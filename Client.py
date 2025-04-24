import socket
import pickle
from main import *

#server = "34.220.181.17"
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

    send_message(client_socket, data.encode())
if mode == "R":
    client_socket.send(b"R")
    #sending room
    send_message(client_socket, room.encode())
    #reciving num of messages
    rawData = receive_message(client_socket)
    num = int(rawData.decode())
    if num == 0:
        print("No messages in room")
        exit(1)
    elif num >= 1:
        print("There are " + str(num) + " messages in the room")
    n = 0
    while n > num or n <= 0 :
        n = int(input("How many messages would you like to receive: "))
    send_message(client_socket, str(n).encode())
    messages = pickle.loads(receive_message(client_socket))
    for x in messages:
        print("Time: " + x.time)
        print("Sender: " + x.sender)
        print(x.message)

client_socket.close()
