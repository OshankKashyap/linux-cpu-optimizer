import time
import platform
import attributes
from pathlib import Path


def checkConfig():
    # function to check whether the configuration file for TLP exists
    # if not create a new file

    path = Path("/etc/tlp.d/00-test.conf")
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
            "CPU_SCALING_MIN_FREQ_ON_AC=400000",
            "CPU_SCALING_MAX_FREQ_ON_AC=3900000",
            "CPU_SCALING_MIN_FREQ_ON_BAT=400000",
            "CPU_SCALING_MAX_FREQ_ON_BAT=3900000"
        ]

        with open(path, "w") as fileObj:
            for x in contents:
                fileObj.write(f"{x}\n")


if __name__ == "__main__":
    PROCESSOR = platform.processor()

    checkConfig()
    attributes.bat.checkThresholdSupport()
    attributes.bat.checkPercentage()

    # if "x86_64" in PROCESSOR or "Intel" in PROCESSOR:
    #     while True:
    #         attributes.cpu.getUsage()
    #         attributes.cpu.setProfile()
    #         time.sleep(1)

    attributes.cpu.getCpuFreq()
