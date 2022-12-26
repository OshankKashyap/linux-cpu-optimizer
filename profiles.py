# Module to contain power profiles

import rw


class Intel:
    def powersave(self):
        # powersave profile
        rw.WriteToFile("CPU_MIN_PERF_ON_AC", 10, True)
        rw.WriteToFile("CPU_MAX_PERF_ON_AC", 100, True)
        rw.WriteToFile("CPU_MIN_PERF_ON_BAT", 10, True)
        rw.WriteToFile("CPU_MAX_PERF_ON_BAT", 37, True)
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


intelProfiles = Intel()
