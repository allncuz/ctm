import socket
import threading

HOST = '127.0.0.1'  # serverning IP-manzili
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

while True:
    msg = input()
    client.send(msg.encode())
    if msg == "end_chat":
        break

client.close()
