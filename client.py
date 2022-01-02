import os, socket, sys, tqdm
from colorama import Fore, init
from cryptography.fernet import Fernet
from datetime import datetime
from threading import Thread

# colours
colour_list = [
    f"{Fore.BLUE}    BLUE:     b{Fore.RESET}",
    f"{Fore.LIGHTCYAN_EX}    CYAN:     c{Fore.RESET}",
    f"{Fore.LIGHTBLACK_EX}    GRAY:     g{Fore.RESET}",
    f"{Fore.LIGHTYELLOW_EX}    LEMON:    le{Fore.RESET}",
    f"{Fore.LIGHTGREEN_EX}    LIME:     li{Fore.RESET}",
    f"{Fore.LIGHTMAGENTA_EX}    MAGENTA:  m{Fore.RESET}",
    f"{Fore.MAGENTA}    PURPLE:   p{Fore.RESET}",
    f"{Fore.RED}    RED:      r{Fore.RESET}",
    f"{Fore.LIGHTRED_EX}    SALMON:   s{Fore.RESET}",
    f"{Fore.LIGHTBLUE_EX}    SKY BLUE: sb{Fore.RESET}",
    f"{Fore.YELLOW}    YELLOW:   y{Fore.RESET}",
    ]

def colour_function(colour_chooser):       
    if colour_chooser.lower() == "b" or colour_chooser.lower() == "blue":
        return Fore.BLUE

    elif colour_chooser.lower() == "c" or colour_chooser.lower() == "cyan":
        return Fore.LIGHTCYAN_EX

    elif colour_chooser.lower() == "g" or colour_chooser.lower() == "gray" or colour_chooser.lower() == "grey":
        return Fore.LIGHTBLACK_EX

    elif colour_chooser.lower() == "le" or colour_chooser.lower() == "lemon":
        return Fore.LIGHTYELLOW_EX

    elif colour_chooser.lower() == "li" or colour_chooser.lower() == "lime":
        return Fore.LIGHTGREEN_EX

    elif colour_chooser.lower() == "m" or colour_chooser.lower() == "magenta":
        return Fore.LIGHTMAGENTA_EX

    elif colour_chooser.lower() == "p" or colour_chooser.lower() == "purple":
        return Fore.MAGENTA

    elif colour_chooser.lower() == "r" or colour_chooser.lower() == "red":
        return Fore.RED

    elif colour_chooser.lower() == "s" or colour_chooser.lower() == "salmon":
        return Fore.LIGHTRED_EX

    elif colour_chooser.lower() == "sb" or colour_chooser.lower() == "skyblue" or colour_chooser.lower() == "sky blue":
        return Fore.LIGHTBLUE_EX

    elif colour_chooser.lower() == "y" or colour_chooser.lower() == "yellow":
        return Fore.YELLOW

    else:
        return Fore.LIGHTWHITE_EX

def cls():
    _ = os.system('cls')


# encryption
def get_key():
    return Fernet(b'81a_yR9CuZk3HzPHocYMWNGUKMYylAO7UQMymGFv9mg=')

def decrypt(input):
    f = get_key()
    return f.decrypt(str(input).encode())

def encrypt(input):
    f = get_key()
    return f.encrypt(bytes(input, encoding='utf8')).decode()


# for timestamps
def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

# send file
def send_file(filename, host, port):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 1024 * 4 #4KB
    filesize = os.path.getsize(filename)
    # to send:
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # send file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

# get msg
def listen_for_messages():
    while True:
        try:
            rcvd = s.recv(1024)
            msg = rcvd.decode()
            decrypted = decrypt(msg)
            print("\n" + str(decrypted.decode()))
        except: pass


def help():
    cmds = '''
    !quit:         quit
    !changecolour: change colour
    !changename:   change username
    !sendfile:     send a file (from same directory as application)
    !help:         see this menu
    '''
    return cmds


cls()
init()

# preference file
# send images

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = ": "

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

try:
    s.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print("[!] Unable to connect.")
    print(f"[!] Error2: {e}")
else:
    print("[+] Connected.")

startup = input("\n\nView help commands?\ny/N: ")

if startup.lower().startswith("n"): pass
else: print(help())
    

name = input("\n\nEnter your username: ")
if name == "":
    name = "anon"
print()

for item in colour_list:
    print(item)

colour_chooser = input(f"\nPick your colour: ")
client_color = colour_function(colour_chooser)

print("\nMessages will look like this:")
print(f"{client_color}[{now()}] {name}: \x1B[3m\x1B[1myour message\x1B[0m{Fore.RESET}")

input("\n\nPress RETURN to connect to the main thread")
cls()

join = f"{name}<SEP>[+] Client connected: {client_color}{name} has joined the chat{Fore.RESET}\n"
encrypted = encrypt(join)
try:
    s.send(str(encrypted).encode())
except Exception as e:
    print(f"[!] Error: {e}")
    sys.exit()

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()
    msg = to_send.lower()

    if msg == '!help':
        print(help())

    elif msg == '!quit':
        exitmsg = f'{client_color}[-] Client disconnect: {name} has left the chat{Fore.RESET}'
        encrypted = encrypt(exitmsg)
        try:
            s.send(str(encrypted).encode())
        except Exception as e:
            print(f"[!] Error: {e}")
        s.close()
        sys.exit()

    elif msg == '!changecolour':
        for item in colour_list:
            print(item)

        client_color = colour_function()
    
    elif msg == '!changename':
        name = input("\nEnter your new username: ")
        print()

    elif msg == '!sendfile':
        name = input("\nEnter your new username: ")
        print()

    elif msg == '':
        pass

    else:
        to_send = f"{client_color}[{now()}] {name}{separator_token}{to_send}{Fore.RESET}"
        encrypted = encrypt(to_send)
        try:
            s.send(str(encrypted).encode())
        except Exception as e:
            print(f"[!] Error: {e}")
            sys.exit()
