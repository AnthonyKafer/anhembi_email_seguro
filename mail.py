
def make_key(s: str) -> int:
  
    return sum(ord(ch) for ch in s)


def make_key_to_server(s: str) -> int:
    return int(sum(ord(char) - 2 for char in s))


def encript(s: str, key: int) -> str:
    parts = []
    for i, ch in enumerate(s):
        code = ord(ch) + key + (i or 1)
        parts.append(chr(code))
    return "^".join(parts)


def decript(s: str, key: int) -> str:
    parts = []
    for i, piece in enumerate(s.split("^")):
        if not piece:
            continue
        ch = piece[0]  
        code = ord(ch) - key - (i or 1)
        parts.append(chr(code))
    return "".join(parts)
