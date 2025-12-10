import socket

import file

PORT = 8080
HOST = '0.0.0.0' #Placeholder
USING_JSON = True
USING_BIN = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(PORT, HOST)

def bindSocketConnection() :
    s.bind((socket.gethostname(), PORT))
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

def closeSocketConnection() :
    s.close

def sendData(data) : 
    #Check if json format 
    s.sendall(formatJsonData(data))



