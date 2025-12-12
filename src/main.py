import sys
import datetime
import time

import file
import client
import temp

def main():
    print("Program startup")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    start_time = time.time()

    try:
        client_instance = client.SocketConnection()
        client_instance.setJsonPreffered(True)

        temp_data = client_instance.getData()
        temp_stat = temp.TEMP_STAT()

        client_instance.sendDataEntry(temp_stat)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        if 'client_instance' in locals():
            if hasattr(client_instance, 'close'):
                client_instance.close()
            else:
                del client_instance

        print("Program shutdown")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("--- %s seconds ---" % (time.time() - start_time), "Runtime")

if __name__ == "__main__":
    main()
