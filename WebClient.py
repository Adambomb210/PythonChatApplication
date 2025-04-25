import socket
import pickle
from main import *
from nicegui import ui

#server = "34.220.181.17"
server = "localhost"
port = 8080

def send_chat(room, username, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server, port))

    client_socket.send(b"W")

    data = room + "\n" + username + "\n" + message

    send_message(client_socket, data.encode())

    client_socket.close()

def render_messages(room, username):
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
            sent = True).style('display: flex; justify-content: flex-end; padding-right: 50px; width: 100vw;')
        else:
            ui.chat_message(x.message,
            stamp = x.time,
            name = x.sender,
            sent = False)
    client_socket.close()

def popup(contents):
    with ui.dialog() as dialog, ui.card():
        ui.label(str(contents))
        ui.button('Close', on_click=dialog.close)

@ui.page("/")
def home():
    with ui.element('div').style('''
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    flex-direction: column;
    gap: 20px
    '''):
        ui.label("Hello! This is my APCSP project, a chat app! It works by a bunch of dark magic behind the scenes, but all you need to know is that to use it, just pick a chat room (it can be any string) and set your username here. Then press go, and it will bring you to the chatroom.").style("width: 50vw; text-align: center")
        room = ui.input(label="Room: ")
        room.style("width: 50vw")
        username = ui.input(label="Username: ")
        username.style("width: 50vw")
        def gps():
            ui.navigate.to(f'/{room.value}/{username.value}')
        ui.button("Go!", on_click=lambda: gps()).style("margin-top: 50px")

@ui.page('/{room}/{username}')
def chatWindow(room: str, username: str):
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('Home')
        ui.button(on_click=lambda: ui.navigate.to("/"), icon='menu').props('flat color=white')
    render_messages(room, username)
    #https://nicegui.io/documentation/textarea
    with ui.footer().style('background-color: #3874c8; height: 25%'):
        message = ui.textarea(label='Text', placeholder='start typing')
        message.style('width: 100%; resize: vertical')
        def handle_submit():
            send_chat(room, username, message.value)
            message.value = ""
            ui.navigate.to(f'/{room}/{username}')
        ui.button("Send", on_click=lambda: handle_submit())

ui.run(port= 80, dark= True)