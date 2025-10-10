# mail.py

def make_key(s: str) -> int:
    # cria uma chave que apenas o usuário e o destino conhecem
    # a chave é uma soma de cada código de caractere das letras do nome do destino
    return sum(ord(ch) for ch in s)


def make_key_to_server(s: str) -> int:
    return int(sum(ord(char) - 2 for char in s))


def encript(s: str, key: int) -> str:
    # encripta a mensagem com a chave sendo o nome do destino
    parts = []
    for i, ch in enumerate(s):
        code = ord(ch) + key + (i or 1)
        parts.append(chr(code))
    return "^".join(parts)


def decript(s: str, key: int) -> str:
    # decripta a mensagem usando o nome do receptor, nome que só ele e o emissor têm acesso
    parts = []
    for i, piece in enumerate(s.split("^")):
        if not piece:
            continue
        ch = piece[0]  # usa apenas o primeiro caractere, como o charCodeAt() do JS
        code = ord(ch) - key - (i or 1)
        parts.append(chr(code))
    return "".join(parts)
