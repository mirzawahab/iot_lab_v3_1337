import network
import time
import BlynkLib
from machine import Pin, I2C
import dht
import ssd1306

# Wi-Fi Credentials
WIFI_SSID = "Mirza Wahab 1"
WIFI_PASS = "wahab973"

# Blynk Auth Token
BLYNK_AUTH = "jAvsLJXx1rKK1e0VIkoT0AZ_7W8gwNnA"

# DHT Sensor Setup
DHT_PIN = 4  # Change according to your ESP32 GPIO
dht_sensor = dht.DHT11(Pin(DHT_PIN))  # Use dht.DHT11 if using DHT11

# OLED Display Setup
I2C_SCL = 9  # Adjust based on your board
I2C_SDA = 8  # Adjust based on your board
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

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

# Function to update temperature and humidity
def update_sensor():
    try:
        dht_sensor.measure()  # Read data from sensor
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        print(f"Temperature: {temp}°C | Humidity: {hum}%")

        # Send data to Blynk
        blynk.virtual_write(0, temp)  # Send temperature to V0
        blynk.virtual_write(1, hum)   # Send humidity to V1

        # Display on OLED
        oled.fill(0)  # Clear screen
        oled.text(f"Temp: {temp} C", 10, 20)
        oled.text(f"Hum: {hum} %", 10, 40)
        oled.show()

    except Exception as e:
        print("Sensor error:", e)

# Main Loop
while True:
    update_sensor()  # Read and update data
    blynk.run()  # Run Blynk
    time.sleep(2)  # Delay before next update
