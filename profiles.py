# Module to contain power profiles

import rw
import psutil


class Main:
    def __init__(self):
        cpuFreq = psutil.cpu_freq()
        self.min = int(cpuFreq.min * 1000000)
        self.max = int(cpuFreq.max * 1000000)

    def powersave(self):
        # powersave profile

        # reduce maximum cpu frequency
        self.max -= int(self.max * 0.585)

        # write chagnes to config file
        # cpu frequencies will be set to maximum if the device is on AC
        rw.WriteToFile("CPU_SCALING_MIN_FREQ_ON_AC", self.min, True)
        rw.WriteToFile("CPU_SCALING_MAX_FREQ_ON_AC", self.max, True)
        rw.WriteToFile("CPU_SCALING_MIN_FREQ_ON_BAT", self.min, True)
        rw.WriteToFile("CPU_SCALING_MAX_FREQ_ON_BAT", self.max, True)

        rw.restartTLP()


profiles = Main()
