import socket
import threading

clients = {}

def green_message(msg):
    print(f"\033[92m{msg}\033[0m")  # Green text

def yellow_message(msg):
    print(f"\033[93m{msg}\033[0m")  # Yellow text

def handle_client(conn, addr):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            print(message)
            if "declareSelf:" in message:
                try:
                    key = int(message.split("declareSelf:")[1])
                except (IndexError, ValueError):
                    continue
                if key in clients:
                    conn.sendall(b"double")
                    continue
                clients[key] = conn
                continue

            if "--" in message:
                try:
                    destiny_code = int(message.split("--")[1])
                except (IndexError, ValueError):
                    continue
                destiny_socket = clients.get(destiny_code)
                is_same_user = (destiny_socket == conn)
                if destiny_socket and not is_same_user:
                    try:
                        destiny_socket.sendall(message.encode())
                        conn.sendall(b"true")
                    except:
                        pass
                else:
                    conn.sendall(b"same" if is_same_user else b"false")
    finally:
        yellow_message("Client disconnected")
        # Remove client from clients dict
        for key, sock in list(clients.items()):
            if sock == conn:
                del clients[key]
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 3000))
    server.listen()

    green_message("Server running on port 3000")

    while True:
        conn, addr = server.accept()
        green_message("Novo usuário conectado")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()