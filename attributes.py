# Module to managing attributes for TLP

import os
import rw
import psutil


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
    def getUsage(self):
        # method to get cpu usage
        self.usage = psutil.cpu_percent()
        return self.usage
    
    def setProfile(self):
        # method to set different profiles based on CPU utilization
        pass


bat = Battery()
cpu = CPU()
