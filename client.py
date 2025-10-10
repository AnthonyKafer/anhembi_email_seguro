import socket
import sys
import re
import threading
from mail import decript, encript, make_key, make_key_to_server
from customConsole import green_message, yellow_message, red_message, message_received

# o nome é declarado pelo usuário antes de rodar o programa, e é recebido do process.argv, uma api do python
#  o operador ! inverte a condição, um if só é ativado se sua condição for verdadeira
#  logo o if só é ativado se o usuário não tiver declarado um nome
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = sys.argv[1] if len(sys.argv) > 1 else None

if not name:
    raise SystemExit(red_message("Você não pode entrar sem um nome"))

yellow_message("\nPara enviar mensagens escreva o nome do destinatário seguido da mensagem")
yellow_message("Exemplo")
yellow_message("Nome: Olá\n\n")

#  usa o objeto do socket do cliente, define no primeiro argumento a porta do servidor
#  e no segundo o host, por ser local é "localhost", o terceiro argumento é uma callback que define
#  o que será feito assim que o usuário se conectar
try:
    client.connect(("localhost", 3000))
except ConnectionRefusedError:
    red_message("Não foi possível conectar ao servidor.")
    sys.exit(1)

green_message("Conectado ao servidor!")
client.sendall(f"declareSelf:{make_key_to_server(name)}".encode())
green_message(f"Conectado com o nome {name}")


def handle_data(data: bytes):
    raw = data.decode().strip()

    if raw == "double":
        red_message("Já existe um usuário com este nome")
        client.close()
        sys.exit(0)
    elif raw == "true":
        green_message("Mensagem enviada com sucesso!")
        return
    elif raw == "false":
        red_message("O usuário não existe ou não está conectado")
        return
    elif raw == "same":
        yellow_message("Você não pode enviar mensagens para si mesmo")
        return

    # Mensagem recebida
    message_received("Você recebeu uma mensagem!", raw)
    try:
        descripted = decript(raw, make_key(name))
        message = descripted.split(":", 1)[1]
        sender, destiny = descripted.split(":", 1)[0].split("/")
        
        yellow_message("Sua mensagem descriptografada")
        message_received(f"De {sender} para {destiny}", message)
    except Exception as e:
        red_message(f"Erro ao descriptografar mensagem: {e}")

    print("> ", end="", flush=True)


def receive_messages():
    while True:
        try:
            data = client.recv(4096)
            if not data:
                red_message("Servidor desconectado.")
                break
            handle_data(data)
        except (ConnectionResetError, OSError):
            red_message("Conexão perdida com o servidor.")
            break
        except Exception as e:
            red_message(f"Erro ao receber mensagem: {e}")
            continue

    client.close()
    sys.exit(0)


def main_loop():
    try:
        while True:
            line = input(": ")

            if line.strip().lower() == "exit":
                client.close()
                red_message("Desconectado")
                break

            destiny_match = re.match(r"^(.*?):", line)
            destiny_name = destiny_match.group(1).strip() if destiny_match else None

            if not destiny_name:
                yellow_message("É necessário declarar um destinatário como abaixo:\nNome: ")
                continue

            if ":" not in line:
                yellow_message("Formato inválido. Use: Nome: mensagem")
                continue

            message_body = line.split(":", 1)[1]
            payload = f"{encript(f'{name}/{destiny_name}:{message_body}', 
            make_key(destiny_name) )}--{make_key_to_server(destiny_name)}"

            client.sendall(payload.encode())
    except KeyboardInterrupt:
        client.close()
        print()
        red_message("Desconectado")


threading.Thread(target=receive_messages, daemon=True).start()
main_loop()
