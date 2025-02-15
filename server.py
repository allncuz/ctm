import socket
import threading
from tunnle import handle_client, clients

HOST = '0.0.0.0'  # server barcha IP-larga ochiq bo‘ladi
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"server {HOST}:{PORT} da ishlayapti...")

while True:
    conn, addr = server.accept()
    conn.send("foydalanuvchi nomingizni kiriting: ".encode())
    username = conn.recv(1024).decode().strip()

    if username in clients:
        conn.send("bu username allaqachon band.\n".encode())
        conn.close()
    else:
        clients[username] = (conn, addr)
        print(f"{username} (IP: {addr[0]}) ulandi.")
        conn.send("chatga xush kelibsiz! mavjud userlarni ko‘rish uchun 'list' yozing.\n".encode())
        threading.Thread(target=handle_client, args=(conn, addr, username), daemon=True).start()

# echo "# .github" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/allncuz/ctm.git
# git push -u origin main

# git remote add origin https://github.com/allncuz/.github.git
# git branch -M main
# git push -u origin main