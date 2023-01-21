import time
import platform
import attributes

if __name__ == "__main__":
    PROCESSOR = platform.processor()

    attributes.bat.checkThresholdSupport()
    attributes.bat.checkPercentage()

    if "x86_64" in PROCESSOR or "Intel" in PROCESSOR:
        while True:
            attributes.cpu.getUsage()
            attributes.cpu.setProfile()
            time.sleep(1)
