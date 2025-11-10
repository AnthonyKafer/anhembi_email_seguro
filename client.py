import socket
import sys
import threading 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def print_prompt():
    print("\nDigite 'login username password' para entrar ou 'register username password' para se registrar.")
    print("Exemplo: login meu_usuario minha_senha")
    print("Depois de logado, use: Nome_destinatario: Mensagem")
    print("Digite 'exit' para sair.")

def handle_data(data: bytes):
    print(data.decode(), end="")

def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break  
            handle_data(data)
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            break

def main():
    try:
        client.connect(("localhost", 3000))
        print_prompt()

        while True:
            user_input = input(": ").strip()

            if user_input.lower() == "exit":
                client.sendall(b"exit")
                print("Desconectado.")
                break

            client.sendall(user_input.encode())
            response = client.recv(1024)
            handle_data(response)

            if "Bem-vindo" in response.decode():
                break  

        threading.Thread(target=receive_messages, daemon=True).start()

        while True:
            recipient = input("\nPara enviar uma mensagem, digite o nome do destinatário e a mensagem:\nNome: Mensagem\nOu 'exit' para sair\n> ")
            if recipient.lower() == "exit":
                client.sendall(b"exit")
                print("Desconectado.")
                break

            if ":" not in recipient:
                print("Formato inválido. Use: Nome: mensagem")
                continue

            client.sendall(recipient.encode())
            response = client.recv(1024)
            handle_data(response)

    except Exception as e:
        print(f"Erro no cliente: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
