def green_message(message: str):
    print(f"\033[32m{message}\033[0m")


def yellow_message(message: str):
    print(f"\033[33m{message}\033[0m")


def red_message(message: str):
    reset = "\033[0m"
    red_bg = "\033[41m"
    white_fg = "\033[97m"
    text = f"{red_bg}   {white_fg}{message}   {reset}"
    print(text)
    return message  


def message_received(message_type: str, raw: str):
    reset = "\033[0m"
    green_bg = "\033[42m"
    blue_bg = "\033[44m"

    text = f"{green_bg}   {message_type}   {reset}"
    print("\n", text)
    print(f"{blue_bg}   {raw}   {reset}\n\n")