import socket,time
import threading,json
from main import get_ncss_from_code,update_stock_from_code,total_sell_update

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT!'



def handle_client(conn, addr):
    print(f'[New connection] {addr} connected.')

    connected = True
    while connected:
        msg_type = conn.recv(4).decode(FORMAT)
        if msg_type:
            if msg_type == 'str ':
                msg_len = conn.recv(HEADER).decode(FORMAT)
                msg = conn.recv(int(msg_len)).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f'[{addr}] {DISCONNECT_MESSAGE}')
                    send_data = json.dumps({'data': 'sended'})
                    send_data_len = str(len(send_data)).encode(FORMAT)
                    send_data_len += b' ' * (HEADER - len(send_data))
                    conn.send(send_data_len)
                    conn.sendall(bytes(send_data, encoding=FORMAT))
                elif msg != DISCONNECT_MESSAGE:
                    print(f'[{addr}] {msg}')
                    print(f'[SENDING {addr}] {get_ncss_from_code(str(msg))}')
                    send_data = json.dumps(get_ncss_from_code(str(msg)))
                    send_data_len = str(len(send_data)).encode(FORMAT)
                    send_data_len += b' ' * (HEADER - len(send_data))
                    conn.send(send_data_len)
                    conn.sendall(bytes(send_data, encoding=FORMAT))

            elif msg_type == 'dict':
                msg_len = conn.recv(HEADER).decode(FORMAT)
                msg = conn.recv(int(msg_len)).decode(FORMAT)
                msg = json.loads(msg)
                print(f'[{addr}] {msg}')
                #update database
                update_stock_from_code(msg['Code'],msg['Quantity'])
                total_sell_update(msg['All'])
                #return data
                send_data = json.dumps({'data': 'sended'})
                send_data_len = str(len(send_data)).encode(FORMAT)
                send_data_len += b' ' * (HEADER - len(send_data))
                conn.send(send_data_len)
                conn.sendall(bytes(send_data, encoding=FORMAT))
                
    conn.close()


def start():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f'[Listening] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        #+print(f'[Active connection] {threading.active_count() -1}')

def close():
    server.close()
    print ("[Server] closed")
