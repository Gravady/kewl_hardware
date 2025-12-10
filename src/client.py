import socket
import json
import time
import threading

PORT = 8080
HOST = '0.0.0.0'   # Listen on all interfaces
DEFAULT_HOST = '127.0.0.1'


class SocketClient:
    def __init__(self):
        self.socketConn = None
        self.DATA = None
        self.JSON_PREFFERED = True
        self.NEW_DATA = None
        self.HAS_NEW_DATA = False
        self.IS_RUNNING = False 

        self.connect()
        self.waitForData()

    def __del__(self):
        self.closeSocketConnection()

    def setJsonPreffered(self, preffered) :
        self.JSON_PREFFERED = preffered

    def connect(self):
        try :
            self.socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketConn.connect(HOST, PORT)
            print(f"Server connected to {HOST}:{PORT}")
            self.IS_RUNNING = True
            threading.Thread(target=self.waitForData, deamon=True).start()
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
            while self.IS_RUNNING:
                raw_data = self.socketConn.recv(1024)
                if not raw_data:
                    print("Server closed connection")
                    break
                self.DATA = deformatJsonData(raw_data.decode('utf-8'))
                if self.DATA is not None :
                    self.NEW_DATA = self.DATA
                print("Received:", self.DATA)
                time.sleep(120)
        except KeyboardInterrupt:
            pass
        finally:
            self.closeSocketConnection()

    def sendDataEntry(self, data) : 
        if(self.JSON_PREFFERED) :
            data = formatJsonData(data)
            self.socketConn.sendall(data.encode('utf-8'))
        else : 
            self.socketConn.sendall(data.encode('utf-8'))

    def closeSocketConnection(self):
        if self.socketConn is not None:
            self.socketConn.close()
        if self.socketConn:
            self.socketConn.close()
        print("Connection closed")

    def getData(self) :
        if self.HAS_NEW_DATA :
            self.HAS_NEW_DATA = False
            return self.NEW_DATA
        else :
            print("No new data")
            return self.DATA


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