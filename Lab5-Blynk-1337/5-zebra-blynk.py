#import blynklib_mp as blynklib,,,,, Good
import BlynkLib as blynklib
import network
import uos
import utime as time
from machine import Pin
from neopixel import NeoPixel

WIFI_SSID = 'Shaam'
WIFI_PASS = 'hehe4Times'
BLYNK_AUTH = "l_mqw6Iyq10ytVDYytTg9ub30KdDM9NL"

print("Connecting to WiFi network '{}'".format(WIFI_SSID))
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    time.sleep(1)
    print('WiFi connect retry ...')
print('WiFi IP:', wifi.ifconfig()[0])

print("Connecting to Blynk server...")
blynk = blynklib.Blynk(BLYNK_AUTH)

# Define the pin connected to the NeoPixel
pin = Pin(48, Pin.OUT)
np = NeoPixel(pin, 1)

# Function to set NeoPixel color
def set_color(r, g, b):
    np[0] = (r, g, b)
    np.write()

@blynk.on("V1")
def v1_write_handler(value):
    print(value)
    r, g, b = map(int, value)
    set_color(r, g, b)
    print("RGB Color set to:", r, g, b)


# Blynk Handlers for Virtual Pins

@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(0, 1, 2)  # Sync RGB sliders from the app

@blynk.on("disconnected")
def blynk_disconnected():
    print("Blynk Disconnected!")

# Main Loop
while True:
  blynk.run()
