import os
import rw
import psutil
import profiles
from pathlib import Path


class Battery:
    def checkThresholdSupport(self):
        # check if the battery supports threshold charging and discarging

        files = os.listdir("/sys/class/power_supply/BAT0/")

        # check for threshold files
        if (
            "charge_control_start_threshold" not in files
            and "charge_control_end_threshold" not in files
        ):
            rw.WriteToFile("START_CHARGE_THRESH_BAT0", 0, False)
            rw.WriteToFile("STOP_CHARGE_THRESH_BAT0", 0, False)
        else:
            rw.WriteToFile("START_CHARGE_THRESH_BAT0", 20, True)
            rw.WriteToFile("STOP_CHARGE_THRESH_BAT0", 95, True)

        rw.restartTLP()

    def checkPercentage(self):
        # method to check the battery percentage
        self.percentage = round(psutil.sensors_battery().percent)

    def setProfile(self):
        # method to set power profile based on different battery levels
        profile = "powersave" if self.percentage > 25 else "default"
        return profile


class CPU:
    def __init__(self):
        self.lastProfile = None

    def getUsage(self):
        # method to get cpu usage
        self.usage = psutil.cpu_percent()

    def setProfile(self):
        # method to set different profiles based on CPU utilization
        PROFILES = ["powersave", "balanced", "performance"]

        '''to avoid changing the profile everytime this functions runs
        the function will check if the current profile needed to be changes is same as the previous profile
        and avoid changing the profile if both are same and changes if the previous profile is different'''
        if self.usage < 15:
            if self.lastProfile == PROFILES[0]:
                rw.restartTLP()
            else:
                profiles.intelProfiles.powersave()
                self.lastProfile = PROFILES[0]
        elif 15 < self.usage < 25:
            if self.lastProfile == PROFILES[1]:
                rw.restartTLP()
            else:
                profiles.intelProfiles.balanced()
                self.lastProfile = PROFILES[1]  
        elif self.usage > 25:
            if self.lastProfile == PROFILES[2]:
                rw.restartTLP()
            else:
                profiles.intelProfiles.performance()
                self.lastProfile = PROFILES[2]
    
    def getCpuFreq(self):
        minFreq = None
        maxFreq = None
        minPath = Path("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq")
        maxPath = Path("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")

        with open(minPath, "r") as fileObj:
            x = fileObj.readline().strip()
            minFreq = int(x)
        
        with open(maxPath, "r") as fileObj:
            x = fileObj.readline().strip()
            maxFreq = int(x)
        
        print(minFreq)
        print(maxFreq)


bat = Battery()
cpu = CPU()
