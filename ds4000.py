import vxi11
import sys
from PIL import Image
import io

class ds4000:
    def __init__(self,ip_address):
        self.instr = vxi11.Instrument(ip_address)
        print(self.instr.ask("*IDN?"))



    def getPNG(self,file_path):
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
        fileName = file_path + "." + "PNG"
        im.save(fileName, "PNG")
        print("Saved file:", "'" + fileName)

    def get_csv(self, file_path):
        # Scan for displayed channels
        chanList = []
        for channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]:
            command = ":" + channel + ":DISP?"
            response = self.instr.ask(command )
            if response == '1':
                chanList += [channel]
        print("Active channels:",chanList)

        self.instr.write(":STOP")
        self.instr.write(":WAV:MODE RAW")

        xincrement = float(self.instr.ask(":WAVeform:XINCrement?"))
        memoryDepth = self.instr.ask(":ACQuire:MDEPth?")

        time_axis =  list(map(float, range(0, 10, 1)))
        time_axis = [x * xincrement for x in time_axis]

        all_channels_data = []
        for channel in chanList:
            self.instr.write(":WAV:SOUR " + channel)
            self.instr.write(":WAV:FORM ASC")


            self.instr.write(":WAVeform:STARt 1")
            self.instr.write(":WAVeform:POINts " + "10")
            data = self.instr.ask(":WAV:DATA?")

            all_channels_data.append([float(i) for i in data.split(',')[:-1]])
        all_channels_data.append(time_axis)
        print(list(zip(*all_channels_data)))





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

