import socket
from cryptography.fernet import Fernet
from datetime import datetime
from os import system
from threading import Thread

def cls():
    _ = system('cls')

def get_key():
    return Fernet(b'81a_yR9CuZk3HzPHocYMWNGUKMYylAO7UQMymGFv9mg=')

def decrypt(input):
    f = get_key()
    return f.decrypt(str(input).encode())

def encrypt(input):
    f = get_key()
    return f.encrypt(bytes(input, encoding='utf8')).decode()

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

def log_file():
    log_name1 = datetime.now().strftime('%Y-%m-%d %H-%M')
    try:
        open(f"{log_name1}.txt", "x")
        return log_name1
    except Exception as e:
        print(f"[!] Error1: {e}")

def log(filename, input):
    with open(f'{filename}.txt', 'a') as log_file:
        log_file.write(input)
        log_file.write('\n')


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"

client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

log_name = log_file()

cls()

listening = f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}"
print(listening)
log(log_name, listening)

def listen(cs, ca):
    while True:
        try:
            rcvd = cs.recv(1024)
            msg = rcvd.decode()

        except Exception as e:
            err = f"[!] Error2: {e}"
            print(err)
            log(log_name, err)
            try:
                client_sockets.remove(cs)
            except:
                c_dc1 = f"[-] Client disconnect: {ca}"
                print(c_dc1)
                log(log_name, c_dc1)
                break
        else:
            decrypted = str(decrypt(msg).decode())
            print(decrypted)

            if separator_token in decrypted:
                print('in')
                split_sep = decrypted.split(separator_token)
                for line in split_sep:
                    line.replace(separator_token, '')
                
                try:
                    print(f'[=] {split_sep[0]} is {ca}')
                    log(log_name, f'[=] {split_sep[0]} is {ca}')
                    log(log_name, split_sep[1])
                except Exception as e:
                    error = f"[!] Error3: {e}"
                    print(error)
                    log(log_name, error)
                    break

                # broadcast
                try:
                    print('trying to send')
                    for client_socket in client_sockets:
                        tosend = encrypt(split_sep[1])
                        print(split_sep[1])
                        
                        client_socket.send(str(tosend).encode())
                        print('sent')
                    print('done')
                except Exception as e:
                    c_dc2 = f"[!] Error4: {e}"
                    print(c_dc2)
                    log(log_name, c_dc2)

            else:
                # broadcast
                try:
                    for client_socket in client_sockets:
                        client_socket.send(msg.encode())    
                except Exception as e:
                    print('err')
                    c_dc2 = f"[!] Error5: {e}"
                    print(c_dc2)
                    log(log_name, c_dc2)

while True:
    client_socket, client_address = s.accept()
    c_c = f"[+] {client_address} connected."
    print(c_c)
    log(log_name, c_c)

    client_sockets.add(client_socket)

    Listen = Thread(target=listen, args=(client_socket,client_address,))
    Listen.daemon = True
    Listen.start()
