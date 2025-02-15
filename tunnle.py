clients = {}  # {"username": (conn, addr)}
tunnels = {}  # {"user1-user2": (conn1, conn2)}

def handle_client(conn, addr, username):
    """har bir foydalanuvchi uchun alohida thread"""
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break

            if msg.startswith("chat "):  # chat boshlash
                target = msg.split()[1]
                if target in clients and target not in tunnels:
                    tunnels[f"{username}-{target}"] = (conn, clients[target][0])
                    conn.send(f"{target} bilan chat boshlandi.\n".encode())
                    clients[target][0].send(f"{username} siz bilan chat boshladi.\n".encode())
                else:
                    conn.send("foydalanuvchi band yoki mavjud emas.\n".encode())

            elif msg == "tunnels":  # aktiv chatlarni ko‘rish
                conn.send(f"aktiv chatlar: {list(tunnels.keys())}\n".encode())

            elif msg == "end_chat":  # chatni yopish
                for key in list(tunnels.keys()):
                    if username in key:
                        conn1, conn2 = tunnels.pop(key)
                        conn1.send("chat yopildi.\n".encode())
                        conn2.send("chat yopildi.\n".encode())
                        break

            else:  # chat xabarlari
                for key, (conn1, conn2) in tunnels.items():
                    if username in key:
                        if conn == conn1:
                            conn2.send(f"{username}: {msg}\n".encode())
                        else:
                            conn1.send(f"{username}: {msg}\n".encode())

        except:
            break

    conn.close()
    del clients[username]
    print(f"{username} (IP: {addr[0]}) chiqdi.")
