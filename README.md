# CPU OPTIMIZER FOR LINUX
This straightforward Linux CPU optimizer was created in Python. Only Intel-based systems using the intel pstate driver are meant for it. To switch between power modes automatically, this script makes use of the [pstate-frequency](https://github.com/pyamsoft/pstate-frequency) driver.

Powersave, balanced, and performance are the three power modes that are currently supported. When the device is charging, the power mode automatically switches to performance, and when it is not attached to a power source, it does the same. It switches to power save mode if the CPU utilization is less than or equal to 15%, switches to balanced mode if the CPU utilization is between 15% and 25%, and switches to performance mode if the CPU utilization is greater than 25%. The device is set to power save mode if the battery life is less than 25%.

To set up, you can refer to the [pstate-frequency](https://github.com/pyamsoft/pstate-frequency) official documentation. Follow the steps below to set up this script:

## BUILD
```
# download the repository
git clone https://github.com/OshankKashyap/linux-cpu-optimizer.git

cd linux-cpu-optimizer
python3 -m venv env

# download the libraries and pyinstaller to create an executable
pip3 install -r requirements.txt

# NOTE: Make sure that you have all the build tools installed
sudo apt install build-essential 
# create an executable
pyinstaller --onefile --name optimizer main.py

cd dist
sudo cp -r optimizer /usr
```

## CREATE SYSTEMD SERVICE
```
sudo touch /lib/systemd/system/cpu-optimizer.service
```

Paste the provided code into the cpu-optimizer.service file after opening it in a text editor as root.
```
[Unit]
Description=python based cpu optimizer

[Service]
Type=simple
ExecStart=/usr/optimizer
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

The service has now been built. You only need to enable and start it at this point.
```
sudo systemctl enable cpu-optimizer.service
sudo systemctl start cpu-optimzer.service
```

Enter the command to check the status of cpu-optimizer.
```
sudo systemctl status cpu-optimizer.service
```
![plot](assets/images/service-status.png)