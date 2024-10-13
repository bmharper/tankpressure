import network
import urequests
import utime
from machine import ADC, Pin
import sys

# Wi-Fi Credentials
ssid = 'YOUR SSID'
password = 'YOUR PASSWORD'
server_addr = '192.168.68.110'
server_port = '8001'

# Initialize LED
led = Pin("LED", Pin.OUT)
led.value(1)

# Initialize ADC
adc = ADC(Pin(26))

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_wifi():
    """Connect to Wi-Fi and handle reconnection."""
    if wlan.isconnected():
        return  # Already connected, skip

    print('Connecting to Wi-Fi...')
    wlan.connect(ssid, password)

    max_wait = 10  # Seconds to wait for connection
    while max_wait > 0:
        if wlan.isconnected():
            print('Connected to Wi-Fi')
            blink(10, 50)  # Indicate successful connection
            return
        print('Waiting for connection...')
        max_wait -= 1
        utime.sleep(1)

    print('Failed to connect to Wi-Fi')
    blink(4, 500)  # Indicate failure
    sys.exit()

def blink(iterations, pause_ms):
    """Blink the onboard LED."""
    for i in range(iterations):
        led.value(i % 2)
        utime.sleep_ms(pause_ms)
    led.value(0)

def send_pressure(adc_value):
    """Send pressure value to the server."""
    url = f'http://{server_addr}:{server_port}/pressure/{adc_value}'
    try:
        response = urequests.get(url)
        print(f'HTTP Response: {response.text}')
        response.close()
    except Exception as e:
        print(f'Error making HTTP request: {e}')
        blink(2, 300)

# Connect to Wi-Fi initially
connect_wifi()

# Send a bogus value so that we know the system is awake
send_pressure(12345)

while True:
    # Ensure Wi-Fi connection is active
    if not wlan.isconnected():
        print('Wi-Fi connection lost. Reconnecting...')
        connect_wifi()

    # Take 60 measurements 1 second apart, and send the median value
    measures = [adc.read_u16() for _ in range(60)]
    utime.sleep(1)  # Delay between each measurement

    median = sorted(measures)[len(measures) // 2]
    send_pressure(median)

    blink(6, 30)  # Indicate data sent
    utime.sleep(60)  # Delay before the next reading
