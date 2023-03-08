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
            rw.WriteToFile("START_CHARGE_THRESH_BAT0", 25, True)
            rw.WriteToFile("STOP_CHARGE_THRESH_BAT0", 95, True)

        rw.restartTLP()

    def checkPercentage(self):
        # method to check the battery percentage
        return round(psutil.sensors_battery().percent)

    def isPlugged(self):
        return psutil.sensors_battery().power_plugged


class CPU:
    def __init__(self):
        self.intelProfiles = profiles.Intel()
        self.lastProfile = None
        self.getCpuFreq()

    def getUsage(self):
        self.cpuUsage = psutil.cpu_percent(interval=0.5)

    def setProfile(self):
        # method to set different profiles based on CPU utilization

        """to avoid changing the profile everytime this functions runs
        the function will check if the current profile needed to be changes is same as the previous profile
        and avoid changing the profile if both are same and changes if the previous profile is different
        """

        if self.cpuUsage < 15:
            if self.lastProfile == "powersave":
                pass
            else:
                self.intelProfiles.powersave()
                self.lastProfile = "powersave"
        elif 15 < self.cpuUsage < 25:
            if self.lastProfile == "balanced":
                pass
            else:
                self.intelProfiles.balanced()
                self.lastProfile = "balanced"
        else:
            if self.lastProfile == "performance":
                pass
            else:
                self.intelProfiles.performance(self.minFreq, self.maxFreq)
                self.lastProfile = "performance"

    def getCpuFreq(self):
        # method to get the minimum and maximum frequency of the cpu

        self.minFreq = None
        self.maxFreq = None
        minPath = Path("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq")
        maxPath = Path("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")

        with open(minPath, "r") as fileObj:
            x = fileObj.readline().strip()
            self.minFreq = int(x)

        with open(maxPath, "r") as fileObj:
            x = fileObj.readline().strip()
            self.maxFreq = int(x)
