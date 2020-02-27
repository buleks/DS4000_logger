import os
import platform
import sys
import ds4000
import time

path_to_save = "output/"
IP_RIGOL = "192.168.1.120"



# Check command line parameters
script_name = os.path.basename(sys.argv[0])


def generateFileName():
    timestamp = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
    return timestamp



def ping_oscilloscope():
    if platform.system() == "Windows":
        response = os.system("ping -n 1 " + IP_RIGOL + " > nul")
    else:
        response = os.system("ping -c 1 " + IP_RIGOL + " > /dev/null")

    if response != 0:
        print ("WARNING! No response pinging " + IP_RIGOL)
        print ("Check network cables and settings.")
        print ("You should be able to ping the oscilloscope.")
        sys.exit('Nothing done. Bye!')


def main():
    global IP_RIGOL
    global path_to_save

    if len(sys.argv) > 1:
        path_to_save = sys.argv[1]
    if len(sys.argv) > 3:
        IP_RIGOL = sys.argv[3]

    ping_oscilloscope()

    rigol = ds4000.ds4000(IP_RIGOL)
    filename = generateFileName()

    # rigol.getPNG(path_to_save+filename)
    # rigol.getCSV(path_to_save+filename)
    print(rigol.getRMS(2))

if __name__== "__main__":
  main()
