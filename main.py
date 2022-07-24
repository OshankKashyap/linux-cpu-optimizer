"""Main module for the program 'linux-cpu-optimizer'
This script automatically change the cpu frequency based on the power requirement
and set to maximum performance when on charging"""

import psutil
import subprocess
import time


class Main:
    def __init__(self):
        self.lastMode = ""

    def getUsage(self) -> None:
        """Method to get the cpu usage and update it at an interval of 1 second"""
        self.cpuUsage = psutil.cpu_percent(interval=0.5)

    def changePowerState(self) -> None:
        """Method to change the power profiles of cpu according to the requirement"""

        commands = {
            "powersave": "sudo /usr/local/bin/pstate-frequency --set --plan powersave",
            "balanced": "sudo /usr/local/bin/pstate-frequency --set --plan balanced",
            "performance": "sudo /usr/local/bin/pstate-frequency --set --plan performance",
        }

        """set cpu frequency -> powersave if cpuUsage < 15 percent
        set cpu frequency -> balanced if cpuUsage > 15 percent
        set cpu frequency -> performance if cpuUsage > 25 percent"""
        # set the self.lastMode variable equal to the last executed profile
        # to avoid changing of powermode each time the function is called

        if self.cpuUsage < 15:
            if self.lastMode == "powersave":
                pass
            else:
                subprocess.call(commands["powersave"], shell=True)
                self.lastMode = "powersave"
        elif 15 < self.cpuUsage < 25:
            if self.lastMode == "balanced":
                pass
            else:
                subprocess.call(commands["balanced"], shell=True)
                self.lastMode = "balanced"
        else:
            if self.lastMode == "performance":
                pass
            else:
                subprocess.call(commands["performance"], shell=True)
                self.lastMode = "performance"


def sleep(duration) -> None:
    # function to stop the execution of the program for a specified time
    time.sleep(duration)


def battery_status() -> bool:
    # function to check if the battery is plugged or not
    plugged = psutil.sensors_battery().power_plugged
    if plugged == True:
        return True
    return False


main = Main()

# main loop
while True:
    main.getUsage()
    plugged = battery_status()
    batteryPercent = int(psutil.sensors_battery().percent)

    # set the powermode to powersave if the battery is lower than 25 percentage
    if batteryPercent < 25 and plugged == False:
        subprocess.call(
            "sudo /usr/local/bin/pstate-frequency --set --plan powersave", shell=True
        )

        # keep on updating the battery percentage until it is greater than 25
        while batteryPercent < 25 and plugged == False:
            batteryPercent = int(psutil.sensors_battery().percent)
            plugged = battery_status()
            sleep(0.5)

    # if the battery is not on charging call the changePowerState() method
    # else set the powermode to performance
    if plugged == False:
        main.changePowerState()
    else:
        subprocess.call(
            "sudo /usr/local/bin/pstate-frequency --set --plan performance", shell=True
        )

        while plugged == True:
            plugged = battery_status()
            sleep(0.5)
