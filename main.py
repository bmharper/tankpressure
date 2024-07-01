import network
import urequests
import utime
from machine import ADC, Pin

# Connect to Wi-Fi
ssid = 'Your SSID'
password = 'Your Password'
server_addr = '192.168.68.107'
server_port = '8001'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

led = Pin("LED", Pin.OUT)
led.value(1)


def blink(iterations, pause_ms):
    for i in range(iterations):
        led.value(i % 2)
        utime.sleep_ms(pause_ms)
    led.value(0)


# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('Waiting for connection...')
    utime.sleep(1)

if not wlan.isconnected():
    print('Failed to connect to WiFi')
    blink(4, 500)
    sys.exit()

print('Connected to WiFi')

blink(10, 50)

# Initialize ADC
adc = ADC(Pin(26))


def read_adc_and_send():
    # Read ADC value
    adc_value = adc.read_u16()

    # Create the URL
    url = f'http://{server_addr}:{server_port}/pressure/{adc_value}'

    try:
        # Make the HTTP GET request
        response = urequests.get(url)
        print(f'HTTP Response: {response.text}')
        response.close()
    except Exception as e:
        print(f'Error making HTTP request: {e}')
        blink(2, 300)


while True:
    read_adc_and_send()
    blink(6, 30)
    utime.sleep(5 * 60)  # Delay between readings
