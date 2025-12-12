import sys 
import datetime
import time

from . import file
from . import client
from . import temp


def main():
    print("Program startup")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    start_time = time.time()
    try : 
        client = client.SocketConnection()
        client.setJsonPreffered(True)
        temp = client.getData()
        temp = temp.TEMP_STAT()
        client.sendDataEntry(temp)
    except KeyboardInterrupt :
        print("Program shutdown")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("--- %s seconds ---" % (time.time() - start_time), "Runtime")
        sys.exit(0)
    finally : 
        client.__del__()
    
    print("Program shutdown")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("--- %s seconds ---" % (time.time() - start_time), "Runtime")

