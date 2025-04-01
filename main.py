import time
import socket
import os
import threading

host = '127.0.0.1'
port = 8080

def send_message(conn, message):
    # Send the length of the message first (4 bytes)
    message_length = len(message)
    conn.send(message_length.to_bytes(4, byteorder='big'))

    # Send the message data in chunks
    conn.sendall(message)

def receive_message(conn):
  # Receive the length of the message first
  message_length_data = conn.recv(4)
  if not message_length_data:
      return None

  # Convert length to integer (assuming 4 bytes for length)
  message_length = int.from_bytes(message_length_data, byteorder='big')

  # Receive the actual message data based on the length
  data = b''  # Empty bytes object to dump the message
  while len(data) < message_length:
      chunk = conn.recv(min(1024, message_length - len(data)))  # Receive in chunks
      if not chunk:
          break  # Connection closed or error
      data += chunk

  return data.decode('utf-8')

def handle_client(conn):
  print("Connected by: " + str(addr))
  mode = conn.recv(1)
  if mode == b"W":
    while True:
      data = receive_message(conn)
      if not data:
          break  # Client disconnected
      print("Received message: " + data)
      #add message handing here
      lines = data.split('\n')
      room = lines[0]
      sender = lines[1]
      message = ""
      for i in range(2, len(lines)):
        message += lines[i] + '\n'
      try:
        with open(room + "\meta.txt", "r+") as file:
          count = int(file.read())

      except FileNotFoundError:
        os.mkdir(room)
        with open(room + "\meta.txt", "w") as file:
          file.write("0")
          count = 0

      with open(room + "\meta.txt", "w+") as file:
        file.write(str(count + 1))

      with open(room + "\\" + str(count) + ".txt", "x") as file:
        file.write(str(time.ctime(time.time())) + "\n" + sender + "\n" + message)
  elif mode == b"R":
    while True:
      data = receive_message(conn)
      if not data:
          break  # Client disconnected
      lines = data.split('\n')
      room = lines[0]
      n = int(lines[1])
      i = -1
      messages = []
      for file in os.scandir(str(room)):
        i += 1
      for x in range(i- n, i):
        if x > 0:
          messages.append(message(x, room))
      send_message(conn, messages)
  conn.close()

class message:
  def __init__(self, count, room):
    self.count = count
    self.room = room
    filename = str(room + "\\" + count + ".txt")
    print(filename)
    try:
      with open(filename, "r+") as file:
        lines = data.split('\n')
        self.time = str(lines[0])
        self.sender = str(lines[1])
        self.message = ""
        for i in range(2, len(lines)):
          self.message += lines[i] + '\n'
    except FileNotFoundError:
      print("File not found: " + filename)  

if __name__ == "__main__":
  mode = input("Enter mode: ")
  if mode == "W":
    sender = input("Username: ")
    message = input("Message: ")
    room = input("Room: ")

    try:
      with open(room + "\meta.txt", "r+") as file:
        count = int(file.read())

    except FileNotFoundError:
      with open(room + "\meta.txt", "w+") as file:
        file.write("0")
        count = 0

    with open(room + "\meta.txt", "w+") as file:
      file.write(str(count + 1))

    with open(room + "\\" + str(count) + ".txt", "x") as file:
      file.write(sender + "\n" + message)

  elif mode == "R":
    room = input("Room: ")
    count = input("Count: ")
    content = message(count, room)
    print("Sender: " + str(content.sender))
    print("Message: " + str(content.message))

  elif mode == "S":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    while True:
      conn, addr = server_socket.accept()
      SThread = threading.Thread(target=handle_client, args=(conn,), daemon = True)
      SThread.start()
  else:
    print("Invalid input.")