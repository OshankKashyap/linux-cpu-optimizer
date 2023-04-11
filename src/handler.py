import time
import attributes
import multiprocessing

cpu = attributes.CPU()
battery = attributes.Battery()


def minBatteryLevel():
    # function to return if the battery level is less than or equal to 25%

    if battery.checkPercentage() <= 25:
        return True

    return False


def process(function, value, stat, mode, modetoChange, priority, myPriority):
    # function to handle different processes

    toCheck = False
    while True:
        with open("testfile.txt", "a") as fileObj:
            fileObj.write(f"Under Process: {myPriority}\n")
            fileObj.write(f"Current Priority: {priority.value}\n")
            fileObj.write(f"Current Mode: {mode.value}\n\n")
        time.sleep(0.5)

        if not toCheck:
            toCheck = False if priority.value < myPriority else True
            continue

        if function() == value:
            while toCheck:
                stat.value = True
                mode.value = modetoChange
                priority.value = myPriority
                toCheck = False if priority.value < myPriority else True


class Handler:
    def __init__(self):
        self.stat = multiprocessing.Value("i")
        self.mode = multiprocessing.Value("i", -1)
        self.priority = multiprocessing.Value("i", 100)
        print(f"Init Priority: {self.priority.value}")

        self.processes = [
            multiprocessing.Process(target=process, args=(attributes.getLidStat, "closed", self.stat, self.mode, 0, self.priority, 1, )),
            multiprocessing.Process(target=process, args=(battery.isPlugged, True, self.stat, self.mode, 2, self.priority, 2, )),
            multiprocessing.Process(target=process, args=(minBatteryLevel, True, self.stat, self.mode, 0, self.priority, 3, )),
            multiprocessing.Process(target=process, args=(battery.isPlugged, False, self.stat, self.mode, -1, self.priority, 4, ))
        ]

    def startProcesses(self):
        # method to start processes

        for process in self.processes:
            process.start()
