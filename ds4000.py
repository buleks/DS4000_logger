import vxi11
import sys
from PIL import Image
import io
import csv





class ds4000:
    def __init__(self,ip_address):
        self.instr = vxi11.Instrument(ip_address)
        print(self.instr.ask("*IDN?"))



    def getPNG(self, file_path):
        self.instr.write(":DISP:DATA?")
        imagebuf = self.instr.read_raw(-1)

        if(chr(imagebuf[0]) != '#'):
            print("Data starting character # not found")
            self.exit()

        headerLen = 9+2
        calculatedBufLen =  headerLen + (800*480*3+54) +1 # 54 is bitmap header

        if len(imagebuf) != calculatedBufLen:
            print("Image length not equal 1152054");
            self.exit()

        #Remove header and new line at the end \n
        imagebuf= imagebuf[headerLen:-1]

        im = Image.open(io.BytesIO(imagebuf))
        file_name = file_path + "." + "PNG"
        im.save(file_name, "PNG")
        print("Saved file:", "'" + file_name)

    def get_fft_csv(self, file_path):
        fft_enabled = self.instr.ask(":CALCulate:MODE?")
        if fft_enabled == "FFT":
            self.instr.write(":WAV:SOUR FFT")
            self.instr.write(":WAV:FORM ASC")

            xincrement = float(self.instr.ask(":WAVeform:XINCrement?"))
            memoryDepth = self.instr.ask(":ACQuire:MDEPth?")
            self.instr.write(":WAVeform:STARt 1")
            self.instr.write(":WAVeform:POINts " + memoryDepth)
            data = self.instr.ask(":WAV:DATA?")
            float_data = [float(i) for i in data.split(',')[:-1]]

            time_axis = list(map(float, range(0, int(memoryDepth), 1)))
            time_axis = [x * xincrement for x in time_axis]

            fft_data = [float_data, time_axis]
            zipped_data = list(zip(*fft_data))

            file_name = file_path + "fft.csv"

            with open(file_name, "w") as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow("FFT data, FFT x axis[Hz]")
                writer.writerows(zipped_data)
            print("Saved file:", "'" + file_name)

    def get_csv(self, file_path):
        # Scan for displayed channels
        chan_list = []
        for channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]:
            command = ":" + channel + ":DISP?"
            response = self.instr.ask(command )
            if response == '1':
                chan_list += [channel]
        # print("Active channels:", chan_list)

        self.instr.write(":STOP")
        self.instr.write(":WAV:MODE NORM")

        xincrement = float(self.instr.ask(":WAVeform:XINCrement?"))
        memoryDepth = self.instr.ask(":ACQuire:MDEPth?")

        time_axis = list(map(float, range(0, int(memoryDepth), 1)))
        time_axis = [x * xincrement for x in time_axis]

        all_channels_data = []
        for channel in chan_list:
            self.instr.write(":WAV:SOUR " + channel)
            self.instr.write(":WAV:FORM ASC")

            self.instr.write(":WAVeform:STARt 1")
            self.instr.write(":WAVeform:POINts " + memoryDepth)
            # print(self.instr.ask(":WAVeform:POINts?"))
            data = self.instr.ask(":WAV:DATA?")
            all_channels_data.append([float(i) for i in data.split(',')[:-1]])
        all_channels_data.insert(0, time_axis)
        zipped_data = list(zip(*all_channels_data))

        file_name = file_path+".csv"

        with open(file_name, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            chan_list.insert(0, "TIME")
            writer.writerow(chan_list)
            writer.writerows(zipped_data)
        print("Saved file:", "'" + file_name)





    def getChannelConfig(self,file_path):

        sampleRate = self.instr.ask(":ACQuire:SRATe?")
        aquisitionType = self.instr.ask(":ACQuire:TYPE?")
        averageCount = self.instr.ask(":ACQuire:AVERages?")

    def getRMS(self,channel):
        channels = ['CHAN1','CHAN2','CHAN3','CHAN4']
        command1 = ":MEASure:VRMs "+channels[channel]
        command2 = ":MEASure:VRMs? "+channels[channel]
        self.instr.write(command1)
        return float(self.instr.ask(command2))



    def close(self):
        self.instr.close()

    def exit(self):
        self.close()
        sys.exit('Nothing done. Bye!')

