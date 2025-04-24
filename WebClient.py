import socket
import pickle
from main import *
from nicegui import ui

#server = "34.220.181.17"
server = "localhost"
port = 8080

def popup(contents):
    with ui.dialog() as dialog, ui.card():
        ui.label(str(contents))
        ui.button('Close', on_click=dialog.close)

if 0 == 1:
    client_socket.send(b"W")
    sender = input("Sender: ")
    message = input("Message: ")

    data = room + "\n" + sender + "\n" + message

    send_message(client_socket, data.encode())


@ui.page('/{room}/{username}')
def chatWindow(room: str, username: str):
    print("Test")
    # Client setup
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server, port))
    client_socket.send(b"R")
    #sending room
    send_message(client_socket, room.encode())
    #reciving num of messages
    rawData = receive_message(client_socket)
    num = int(rawData.decode())
    if num == 0:
        popup("No messages in room")
    send_message(client_socket, str(num).encode())
    messages = pickle.loads(receive_message(client_socket))
    for x in messages:
        if x.sender == username:
            ui.chat_message(x.message,
            stamp = x.time,
            name = x.sender,
            sent = True)
        else:
            ui.chat_message(x.message,
            stamp = x.time,
            name = x.sender,
            sent = False)
    client_socket.close()
    #https://nicegui.io/documentation/textarea
    with ui.footer().style('background-color: #3874c8'):
        ui.textarea(label='Text', placeholder='start typing',
            on_change=lambda e: result.set_text('you typed: ' + e.value))
        result = ui.label()

ui.run(port= 80, dark= True)