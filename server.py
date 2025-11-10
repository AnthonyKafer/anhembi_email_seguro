import socket
import threading
import hashlib
import json

clients = {}  

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save users to JSON file
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def authenticate_user(username: str, password: str) -> bool:
    users = load_users()
    hashed_password = hash_password(password)
    return users.get(username, {}).get("password") == hashed_password

def register_user(username: str, password: str):
    users = load_users()
    if username in users:
        return False  
    users[username] = {"password": hash_password(password)}
    save_users(users)
    return True

def green_message(msg):
    print(f"\033[92m{msg}\033[0m")  

def yellow_message(msg):
    print(f"\033[93m{msg}\033[0m")  

def handle_client(conn, addr):
    try:
        conn.sendall("Bem-vindo! Faça login ou registre-se.\n".encode("utf-8"))
        username = None
        while True:
            data = conn.recv(1024).decode().strip()

            if data.lower().startswith("login"):
                _, username_input, password_input = data.split(" ")
                if authenticate_user(username_input, password_input):
                    username = username_input
                    conn.sendall(f"Login bem-sucedido, {username}!\n".encode("utf-8"))
                    break
                else:
                    conn.sendall("Falha no login. Tente novamente.\n".encode("utf-8"))

            elif data.lower().startswith("register"):
                _, username_input, password_input = data.split(" ")
                if register_user(username_input, password_input):
                    username = username_input
                    conn.sendall(f"Registro bem-sucedido, {username}!\n".encode("utf-8"))
                    break
                else:
                    conn.sendall("Usuário já existe. Tente outro nome.\n".encode("utf-8"))

        clients[username] = conn
        yellow_message(f"Usuário {username} conectado.")

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break 

            if data.lower() == "exit":
                break

            if ":" in data:
                recipient, message = data.split(":", 1)
                recipient = recipient.strip() 
                if recipient in clients:
                    clients[recipient].sendall(f"Mensagem de {username}: {message}\n".encode("utf-8"))
                    conn.sendall(f"Mensagem enviada para {recipient}.\n".encode("utf-8"))
                else:
                    conn.sendall(f"Usuário {recipient} não encontrado.\n".encode("utf-8"))
            else:
                conn.sendall("Formato inválido. Use 'Nome: mensagem'.\n".encode("utf-8"))

    except Exception as e:
        print(f"Erro com o cliente {addr}: {e}")
    finally:
        if username:
            del clients[username]
            yellow_message(f"Usuário {username} desconectado.")
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 3000))  
    server.listen(5) 
    green_message("Servidor rodando na porta 3000...")

    while True:
        conn, addr = server.accept() 
        green_message(f"Novo usuário conectado: {addr}")
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
