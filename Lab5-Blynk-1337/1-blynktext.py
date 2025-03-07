#RGB controling using Blynk cloude text input
import BlynkLib as blynklib
import network
import uos
import utime as time
from machine import Pin, I2C, Timer
from neopixel import NeoPixel
#from machine import Pin, I2C, Timer
import ssd1306

WIFI_SSID = 'Shaam'
WIFI_PASS = 'hehe4Times'
BLYNK_AUTH = "LFLoOevfDpMf2hYol4Wg7SemkAEkW4uk"

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



i2c = I2C(1, scl=Pin(9), sda=Pin(8), freq= 200000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)




# Blynk Handlers for Virtual Pins
@blynk.on("V0")  # Red Slider
def v0_handler(value):
    try:
        # Parse the input text (expected format: "R,G,B")
        oled.fill(0)
        
        oled.text(value[0], 5,5)
        oled.show()
    except Exception as e:
        print("Invalid input:", e)
    
@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(0)  # Sync RGB sliders from the app

@blynk.on("disconnected")
def blynk_disconnected():
    print("Blynk Disconnected!")

# Main Loop
while True:
    blynk.run()
    

