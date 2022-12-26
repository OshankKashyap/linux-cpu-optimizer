import profiles
import attributes
import platform

if __name__ == "__main__":
    PROCESSOR = platform.processor()

    attributes.bat.checkThresholdSupport()
    attributes.bat.checkPercentage()

    if "x86_64" in PROCESSOR or "Intel" in PROCESSOR:
        profiles.intelProfiles.performance()