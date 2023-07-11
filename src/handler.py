import time
import attributes

cpu = attributes.CPU()
battery = attributes.Battery()


def minBatteryLevel():
    # function to return if the battery level is less than or equal to 25%
    return True if battery.checkPercentage() <= 25 else False


class Handler:
    def __init__(self):
        self.mode = None

    def main(self):
        functions = [
            [attributes.getLidStat, "powersave"],
            [battery.isPlugged, "performance"],
            [minBatteryLevel, "powersave"]
            [battery.isPlugged, "auto"],
        ]

        while True:
            for func in functions:
                if func[0]() == True:
                    self.mode = func[1]
                    break
                
                time.sleep(0.5)
            print("")
