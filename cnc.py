import os, time

# --- Gradiente de fondo en el prompt ---
def gradient_block(text, start_rgb=(0,40,90), end_rgb=(150,200,255)):
    result = ""                                                                   length = len(text)                                                            for i, ch in enumerate(text):
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * (i / max(1, length-1)))
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * (i / max(1, length-1)))
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * (i / max(1, length-1)))
        result += f"\033[48;2;{r};{g};{b}m\033[38;2;255;255;255m{ch}"
    return result + "\033[0m"

def build_prompt():
    return gradient_block(" root ● RainC2 ")

PROMPT = build_prompt()

# --- Gradiente azul → blanco para texto normal ---
def gradient_text(text):
    result = ""
    palette = [
        "\033[1;38;2;0;120;255m",
        "\033[1;38;2;50;150;255m",
        "\033[1;38;2;100;180;255m",
        "\033[1;38;2;150;210;255m",
        "\033[1;38;2;200;230;255m",
        "\033[1;97m"
    ]
    step_len = max(1, len(text)//len(palette))
    for i, ch in enumerate(text):
        color_idx = min(i // step_len, len(palette)-1)
        result += palette[color_idx] + ch
    return result + "\033[0m"

# --- Banner ---
BANNER_RAW = r"""
 ██▀███   ▄▄▄       ██▓ ███▄    █
▓██ ▒ ██▒▒████▄    ▓██▒ ██ ▀█   █
▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒▓██  ▀█ ██▒
▒██▀▀█▄  ░██▄▄▄▄██ ░██░▓██▒  ▐▌██▒
░██▓ ▒██▒ ▓█   ▓██▒░██░▒██░   ▓██░
░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▓  ░ ▒░   ▒ ▒
  ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░░ ░░   ░ ▒░
  ░░   ░   ░   ▒    ▒ ░   ░   ░ ░
   ░           ░  ░ ░           ░
"""

WELCOME = "Welcome to RainC2 CNC Premium!\nType 'help' for commands.\n"

# --- Fake Session Info ---
def show_session_info():
    print("\033[1;37m[2] \033[0mKrypton C2 \033[1;37m| Bots online:\033[0m 0 \033[1;37m| Username:\033[0m root \033[1;37m| Expires:\033[0m 2029-12-31\n")

# --- Variables de ataque ---
last_attack = {
    "target": None,
    "port": None,
    "time": 0,
    "method": None,
    "active": False,
    "start_time": None
}

def clear():
    os.system("clear")
    print(gradient_text(BANNER_RAW))
    print(gradient_text(WELCOME))

def help_cmd():
    cmds = [
        "help                     Show this help",
        "servers                  Show available bots",
        "attack <ip/url> <port> <time> udp        Start UDP FLOOD",
        "attack <ip/url> <port> <time> cf_http    Start CF_HTTP Flood",
        "info                     Show last attack info",
        "clear                    Clear the screen",
        "exit                     Quit"
    ]
    print(gradient_text("Available Commands:"))
    for c in cmds:
        print(gradient_text("  " + c))

def servers_cmd():
    print(gradient_text("Available bots: 14"))

def is_url(target):
    return target.startswith("http://") or target.startswith("https://")

def attack_cmd(args):
    global last_attack
    if len(args) != 4 or args[3] not in ["udp", "cf_http"]:
        print(gradient_text("Usage: attack <ip/url> <port> <time> <udp|cf_http>"))
        return

    target, port, duration, method = args
    duration = int(duration)

    last_attack.update({
        "target": target,
        "port": port,
        "time": duration,
        "method": method,
        "active": True,
        "start_time": time.time()
    })

    method_name = "UDP FLOOD" if method == "udp" else "CF_HTTP FLOOD"
    print(gradient_text(f"Attack running ({method_name})..."))

def info_cmd():
    if not last_attack["active"]:
        print(gradient_text("No active attacks at the moment."))
        return

    elapsed = int(time.time() - last_attack["start_time"])
    remaining = max(0, last_attack["time"] - elapsed)

    status = "RUNNING with 14 bots" if remaining > 0 else "FINISHED"
    if remaining == 0:
        last_attack["active"] = False

    method_name = "UDP FLOOD" if last_attack["method"] == "udp" else "CF_HTTP FLOOD"
    target_label = "Target" if is_url(last_attack["target"]) else "Target IP"

    print(gradient_text("➤ Attack Information:"))
    print(gradient_text(f"   {target_label}: {last_attack['target']}"))
    print(gradient_text(f"   Target Port: {last_attack['port']}"))
    print(gradient_text(f"   Time Left: {remaining} seconds"))
    print(gradient_text(f"   Method: {method_name}"))
    print(gradient_text(f"   Status: {status}"))

# --- Main ---
def main():
    os.system("clear")
    show_session_info()  # <<< Muestra el panel fake estilo KryptonC2
    clear()
    while True:
        try:
            cmd_input = input(PROMPT).strip()
            if not cmd_input:
                continue
            parts = cmd_input.split()
            cmd = parts[0]

            if cmd == "help":
                help_cmd()
            elif cmd == "servers":
                servers_cmd()
            elif cmd == "attack":
                attack_cmd(parts[1:])
            elif cmd == "info":
                info_cmd()
            elif cmd == "clear":
                clear()
            elif cmd == "exit":
                print(gradient_text("Goodbye!"))
                break
            else:
                print(gradient_text("Unknown command. Type 'help'."))
        except KeyboardInterrupt:
            print("\n" + gradient_text("Exiting..."))
            break

if __name__ == "__main__":
    main()
