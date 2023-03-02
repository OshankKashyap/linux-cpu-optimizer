import rw
import psutil


class Intel:
    def __init__(self):
        cpuFreq = psutil.cpu_freq()
        self.cpu_min = int(cpuFreq.min * 1000)
        self.cpu_max = int(cpuFreq.max * 1000)

    def powersave(self):
        # powersave profile

        rw.WriteToFile("CPU_MIN_PERF_ON_AC", 10, False)
        rw.WriteToFile("CPU_MAX_PERF_ON_AC", 100, False)
        rw.WriteToFile("CPU_MIN_PERF_ON_BAT", 10, False)
        rw.WriteToFile("CPU_MAX_PERF_ON_BAT", 37, False)
        rw.WriteToFile("CPU_BOOST_ON_AC", 0, True)
        rw.WriteToFile("CPU_BOOST_ON_BAT", 0, True)
        rw.WriteToFile("CPU_SCALING_GOVERNOR_ON_AC", "powersave", True)
        rw.WriteToFile("CPU_SCALING_GOVERNOR_ON_BAT", "powersave", True)

        rw.restartTLP()

    def balanced(self):
        # balanced profile

        rw.WriteToFile("CPU_MIN_PERF_ON_AC", 10, True)
        rw.WriteToFile("CPU_MAX_PERF_ON_AC", 100, True)
        rw.WriteToFile("CPU_MIN_PERF_ON_BAT", 10, True)
        rw.WriteToFile("CPU_MAX_PERF_ON_BAT", 100, True)
        rw.WriteToFile("CPU_BOOST_ON_AC", 1, True)
        rw.WriteToFile("CPU_BOOST_ON_BAT", 1, True)
        rw.WriteToFile("CPU_SCALING_GOVERNOR_ON_AC", "powersave", True)
        rw.WriteToFile("CPU_SCALING_GOVERNOR_ON_BAT", "powersave", True)

        rw.restartTLP()

    def performance(self, cpuMin, cpuMax):
        # performance profile

        rw.WriteToFile("CPU_SCALING_MIN_FREQ_ON_AC", cpuMin, True)
        rw.WriteToFile("CPU_SCALING_MAX_FREQ_ON_AC", cpuMax, True)
        rw.WriteToFile("CPU_SCALING_MIN_FREQ_ON_BAT", cpuMin, True)
        rw.WriteToFile("CPU_SCALING_MAX_FREQ_ON_BAT", cpuMax, True)
        rw.WriteToFile("CPU_MIN_PERF_ON_AC", 10, False)
        rw.WriteToFile("CPU_MAX_PERF_ON_AC", 100, False)
        rw.WriteToFile("CPU_MIN_PERF_ON_BAT", 10, False)
        rw.WriteToFile("CPU_MAX_PERF_ON_BAT", 100, False)
        rw.WriteToFile("CPU_BOOST_ON_AC", 1, True)
        rw.WriteToFile("CPU_BOOST_ON_BAT", 1, True)
        rw.WriteToFile("CPU_SCALING_GOVERNOR_ON_AC", "performance", True)
        rw.WriteToFile("CPU_SCALING_GOVERNOR_ON_BAT", "performance", True)

        rw.restartTLP()

intelProfiles = Intel()
