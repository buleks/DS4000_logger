import os
import platform
import sys
import ds4000
import time
from pynput.keyboard import Key, Listener
import signal

path_to_save = "output/"
IP_RIGOL = "192.168.1.17"

def generateFileName():
    timestamp = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
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

gather_data = False
running = True


def on_press(key):
    global gather_data
    if key == Key.space:
        gather_data = True


def on_release(key):
    global running

    if key == Key.esc:
        print("Quitting...")
        running = False
        return False


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Press ESC to quit.')


def main():
    global IP_RIGOL
    global path_to_save

    if len(sys.argv) > 1:
        path_to_save = sys.argv[1]
    if len(sys.argv) > 2:
        IP_RIGOL = sys.argv[2]

    ping_oscilloscope()

    rigol = ds4000.ds4000(IP_RIGOL)


    # with Listener(
    #         on_press=on_press,
    #         on_release=on_release) as listener:
    #     listener.run()
    listener = Listener( on_press=on_press, on_release=on_release)
    listener.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press Space to acquire data. Pres ESC to quit.")
    global gather_data
    while running:
        time.sleep(1)
        if gather_data:
            print("Processing...")
            filename = generateFileName()
            rigol.getPNG(path_to_save + filename)
            rigol.get_csv(path_to_save + filename)
            rigol.get_fft_csv(path_to_save + filename)
            print("Ready.")
            gather_data = False

    rigol.close()


if __name__ == "__main__":
    main()
