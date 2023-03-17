import time
import profiles
import attributes
from pathlib import Path

bat = attributes.Battery()
cpu = attributes.CPU()


def checkConfig():
    # function to check whether the configuration file for TLP exists
    # if not create a new file

    path = Path("/etc/tlp.d/00-tlp.conf")
    if not path.exists():
        contents = [
            "# Test File",
            "TLP_ENABLE=1",
            "",
            "# Battery Configuration",
            "#START_CHARGE_THRESH_BAT0=0",
            "#STOP_CHARGE_THRESH_BAT0=0",
            "",
            "# CPU Configuration",
            "#CPU_MIN_PERF_ON_AC=10",
            "#CPU_MAX_PERF_ON_AC=100",
            "#CPU_MIN_PERF_ON_BAT=10",
            "#CPU_MAX_PERF_ON_BAT=37",
            "",
            "CPU_BOOST_ON_AC=0",
            "CPU_BOOST_ON_BAT=0",
            "",
            "CPU_SCALING_GOVERNOR_ON_AC=powersave",
            "CPU_SCALING_GOVERNOR_ON_BAT=powersave",
            "",
            f"CPU_SCALING_MIN_FREQ_ON_AC={cpu.minFreq}",
            f"CPU_SCALING_MAX_FREQ_ON_AC={cpu.maxFreq}",
            f"CPU_SCALING_MIN_FREQ_ON_BAT={cpu.minFreq}",
            f"CPU_SCALING_MAX_FREQ_ON_BAT={cpu.maxFreq}",
        ]

        with open(path, "w") as fileObj:
            for x in contents:
                fileObj.write(f"{x}\n")


def main():
    # main function to handle power states based on cpu usage and battery level

    while True:
        plugged = bat.isPlugged()
        batteryPercent = bat.checkPercentage()

        # set the powermode to powersave if the battery is lower than 25 percentage and not plugged
        if batteryPercent < 25 and not plugged:
            profiles.Intel.powersave()

            # keep on updating the battery percentage until it is greater than 25
            while batteryPercent < 25 and not plugged:
                batteryPercent = bat.checkPercentage()
                plugged = bat.isPlugged()
                time.sleep(0.5)

        # if the battery is not on charging change the power modes automatically
        # else set the powermode to performance
        if plugged == False:
            cpu.setProfile()
        else:
            profiles.Intel().performance(cpu.minFreq, cpu.maxFreq)

            while plugged == True:
                plugged = bat.isPlugged()
                time.sleep(0.5)


if __name__ == "__main__":
    checkConfig()

    if cpu.getManufacturer() == "Intel(R)":
        main()
