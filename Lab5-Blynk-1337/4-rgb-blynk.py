#Blynk rgb1 template
#control rgb through 3 sliders
import BlynkLib as blynklib
import network
import uos
import utime as time
from machine import Pin
from neopixel import NeoPixel

WIFI_SSID = 'Shaam'
WIFI_PASS = 'hehe4Times'
BLYNK_AUTH = "_SKT7ThWOHJlwMoPkbx65dwxzm3AUOJR"

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

def set_color(r, g, b):
    np[0] = (r, g, b)
    np.write()

# RGB Values
r = 0
g = 0
b = 0

# Blynk Handlers for Virtual Pins
@blynk.on("V0")  # Red Slider
def v0_handler(value):
    global r
    r = int(value[0])
    set_color(r, g, b)

@blynk.on("V1")  # Green Slider
def v1_handler(value):
    global g
    g = int(value[0])
    set_color(r, g, b)

@blynk.on("V2")  # Blue Slider
def v2_handler(value):
    global b
    b = int(value[0])
    set_color(r, g, b)

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
