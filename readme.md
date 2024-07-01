# RPi2040 (Raspberry Pi Pico W) Tank Pressure Monitor

This is a little combo that I built to measure the tank pressure in my septic tank
using a [Submersible Pressure Level Sensor](https://www.dfrobot.com/product-1863.html).
Every 5 minutes the Pico W wakes up and takes a reading from the ADC, and then sends that
value to another server via HTTP.

## Server Install

1. `pip3 install flask`, or `sudo apt install python3-flask` for Ubuntu
2. `sudo cp tankpressure.service /etc/systemd/system`
3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable tankpressure.service`
5. `sudo systemctl start tankpressure.service`
6. `sudo systemctl status tankpressure.service`

## Client install

1. Set the SSID and password in the `client.py` file, as well as the IP address of the server.
2. Download the MicroPython `.u2f` file from https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
3. Install that `.u2f` file by using the bootsel button an copying the file to the Pico W mass storage
4. Use `thonny` to install `main.py` onto the Pico W. You need to copy `main.py` onto the firmware of the device.
