import os
import rw
import sys
import psutil
import profiles
from pathlib import Path


def getLidStat():
    # function to check whether the LID of laptop is open of closed

    path = Path("/proc/acpi/button/lid/LID/state")
    if os.path.exists(path) and rw.readFile(path)[0].split(" ")[-1].strip() == "closed":
        return True

    return False


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
        try:
            return psutil.sensors_battery().power_plugged
        except Exception:
            print("Error: No Battery Found!")
            sys.exit()

    def notPlugged():
        try:
            return not psutil.sensors_battery().power_plugged
        except Exception:
            print("Error: No Battery Found!")
            sys.exit()


class CPU:
    def __init__(self):
        self.lastProfile = None
        self.intelProfiles = profiles.Intel()
        self.paths = {
            "min_path": Path("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq"),
            "max_path": Path("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"),
            "cpu_info": Path("/proc/cpuinfo"),
        }
        self.getCpuFreq()

    def setProfile(self, mode):
        # method to set different profiles based on CPU utilization

        """to avoid changing the profile everytime this functions runs
        the function will check if the current profile needed to be changes is same as the previous profile
        and avoid changing the profile if both are same and changes if the previous profile is different
        """

        cpuUsage = psutil.cpu_percent(interval=0.5)
        if mode == "auto":
            if cpuUsage < 15:
                if self.lastProfile == "powersave":
                    pass
                else:
                    self.intelProfiles.powersave()
                    self.lastProfile = "powersave"
            elif 15 < cpuUsage < 25:
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
        elif mode == "performance":
            if self.lastProfile == "performance":
                pass
            else:
                self.intelProfiles.performance(self.minFreq, self.maxFreq)
                self.lastProfile = "performance"
        elif mode == "balanced":
            if self.lastProfile == "balanced":
                pass
            else:
                self.intelProfiles.balanced()
                self.lastProfile = "balanced"
        elif mode == "powersave":
            if self.lastProfile == "powersave":
                pass
            else:
                self.intelProfiles.powersave()
                self.lastProfile = "powersave"

    def getCpuFreq(self):
        # method to get the minimum and maximum frequency of the cpu

        self.minFreq = int(rw.readFile(self.paths["min_path"])[0].strip())
        self.maxFreq = int(rw.readFile(self.paths["max_path"])[0].strip())

    def getManufacturer(self):
        # method to get the manufactuer of CPU

        if os.path.exists(self.paths["cpu_info"]):
            return rw.readFile(self.paths["cpu_info"])[4].split(" ")[2]

        return None
