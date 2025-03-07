import network
import time
import BlynkLib
from machine import Pin, I2C
from neopixel import NeoPixel
import ssd1306
import _thread  # Import threading module

# Wi-Fi Credentials
WIFI_SSID = "Mirza Wahab 1"
WIFI_PASS = "wahab973"

# Blynk Auth Token
BLYNK_AUTH = "l_mqw6Iyq10ytVDYytTg9ub30KdDM9NL"

# OLED Display Setup
I2C_SCL = 9  # Adjust based on your board
I2C_SDA = 8  # Adjust based on your board
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def display_text(text):
    oled.fill(0)  # Clear screen
    oled.text(text, 10, 30)
    oled.show()

# Built-in RGB LED on GPIO 48
RGB_PIN = 48
NUM_LEDS = 1  # Only one built-in LED
rgb_led = NeoPixel(Pin(RGB_PIN, Pin.OUT), NUM_LEDS)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)

    print("Connected to Wi-Fi:", wlan.ifconfig())

connect_wifi()

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Function to control RGB LED
def set_color(r, g, b):
    rgb_led[0] = (r, g, b)
    rgb_led.write()

# Handle RGB Color from Zebra Widget on V4
@blynk.on("V4")
def v4_write(value):
    hex_color = value[0]  # Get HEX color from Blynk
    hex_color = hex_color.lstrip('#')  # Remove '#' from HEX code

    # Convert HEX to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    set_color(r, g, b)  # Apply color to LED
    display_text(f"RGB: {r},{g},{b}")  # Show on OLED
    print(f"RGB: {r}, {g}, {b}")  # Debug output

# Blynk Button Handlers
@blynk.on("V0")  # Button for Red
def v0_write(value):
    if int(value[0]) == 1:
        set_color(255, 0, 0)  # Red ON
        display_text("Red ON")
    else:
        set_color(0, 0, 0)  # OFF
        display_text("Red OFF")

@blynk.on("V1")  # Button for Green
def v1_write(value):
    if int(value[0]) == 1:
        set_color(0, 255, 0)  # Green ON
        display_text("Green ON")
    else:
        set_color(0, 0, 0)  # OFF
        display_text("Green OFF")

@blynk.on("V2")  # Button for Blue
def v2_write(value):
    if int(value[0]) == 1:
        set_color(0, 0, 255)  # Blue ON
        display_text("Blue ON")
    else:
        set_color(0, 0, 0)  # OFF
        display_text("Blue OFF")

# Light show effect
light_show_active = False

def light_show():
    global light_show_active
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
        (255, 255, 255) # White
    ]
    
    while light_show_active:
        for r, g, b in colors:
            for i in range(0, 256, 25):  # Fade In
                if not light_show_active:
                    return  # Stop animation immediately
                set_color(int(r * (i / 255)), int(g * (i / 255)), int(b * (i / 255)))
                time.sleep(0.01)
            
            for i in range(255, -1, -25):  # Fade Out
                if not light_show_active:
                    return  # Stop animation immediately
                set_color(int(r * (i / 255)), int(g * (i / 255)), int(b * (i / 255)))
                time.sleep(0.01)

@blynk.on("V3")  # Button for Light Show
def v3_write(value):
    global light_show_active
    if int(value[0]) == 1:
        light_show_active = True
        display_text("Light Show ON")
        _thread.start_new_thread(light_show, ())  # Run animation in a separate thread
    else:
        light_show_active = False
        set_color(0, 0, 0)  # Turn off LED
        display_text("Light Show OFF")

# Main Loop
while True:
    blynk.run()

