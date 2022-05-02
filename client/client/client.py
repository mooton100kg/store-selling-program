import socket,json

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT!'

def start(SERVER : str):
    ADDR = (SERVER, PORT)
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

def send(type,msg,out_data):
    send_type = type.encode(FORMAT)
    client.send(send_type)
    print(f'[SENDING] {msg}')
    if type == 'str ':
        send_data = msg.encode(FORMAT)
        send_len = str(len(send_data)).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        client.send(send_len)
        client.send(send_data)
    elif type == 'dict':
        send_data = json.dumps(msg)
        send_len = str(len(send_data)).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        client.send(send_len)
        client.sendall(bytes(send_data, encoding=FORMAT))

    return_data_len = client.recv(HEADER).decode(FORMAT)
    return_data = client.recv(int(return_data_len)).decode(FORMAT)
    return_data = json.loads(return_data)
    out_data.append(return_data)




