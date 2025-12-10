import socket
import json
import time

PORT = 8080
HOST = '0.0.0.0'   # Listen on all interfaces
DEFAULT_HOST = '127.0.0.1'


class SocketConnection:
    def __init__(self):
        self.socketConn = None
        self.CONN = None
        self.DATA = None
        self.JSON_PREFFERED = True
        
        self.connectSocketConnection()
        self.waitForData()

    def __del__(self):
        self.closeSocketConnection()

    def setJsonPreffered(self, preffered) :
        self.JSON_PREFFERED = preffered

    def connectSocketConnection(self):
        try :
            self.socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketConn.connect(HOST, PORT)
            print(f"Server listening on {HOST}:{PORT}")
            self.CONN, addr = self.socketConn.accept()
            print("Connected by", str(addr))
        except KeyboardInterrupt:
            pass
        except OSError as e:
            print("Connection failed on primary host")
            try : 
                print("Attempting default localhost connection")
                self.socketConn.connect(DEFAULT_HOST, PORT)
            except OSError as e :
                print(e)
            return 
        except Exception as e:
            print(e)
            return

    def waitForData(self):
        try:
            while True:
                self.DATA = deformatJsonData(self.CONN.recv(1024).decode('utf-8'))
                #Forward data to hardware_controller.py
                if not self.DATA:
                    break
                print("Received:", self.DATA)
                time.sleep(120)
        except KeyboardInterrupt:
            pass
        finally:
            self.closeSocketConnection()

    def sendDataEntry(self, data) : 
        if(self.JSON_PREFFERED) :
            data = formatJsonData(data)
            self.CONN.sendall(data.encode('utf-8'))
        else : 
            data = deformatJsonData(data)
            self.CONN.sendall(data.encode('utf-8'))

    def closeSocketConnection(self):
        if self.CONN:
            self.CONN.close()
        if self.socketConn:
            self.socketConn.close()
        print("Connection closed")


def formatJsonData(data):
    try :
        return json.dumps(data)
    except ValueError as e:
        print("Invaid json format")

def deformatJsonData(data) :
    try : 
        return json.loads(data)
    except ValueError as e :
        print("Invaid json format")
        return