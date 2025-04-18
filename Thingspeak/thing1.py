import machine
import dht
import urequests
import time
import ujson
from machine import Pin, SoftI2C
import ssd1306

# Configuration
THINGSPEAK_API_KEY = "U18ZKTN3RL7YXUNG"
THINGSPEAK_WRITE_URL = "https://api.thingspeak.com/update"
DHT_PIN = 4
CHECK_INTERVAL = 20

# Initialize hardware
dht_sensor = dht.DHT11(Pin(DHT_PIN))
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def read_sensor():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except Exception as e:
        print("Sensor read error:", e)
        return None, None

def send_to_thingspeak(temp, humidity):
    try:
        url = f"{THINGSPEAK_WRITE_URL}?api_key={THINGSPEAK_API_KEY}&field1={temp}&field2={humidity}"
        response = urequests.get(url)
        print("ThingSpeak update:", response.text)
        response.close()
        return True
    except Exception as e:
        print("ThingSpeak send error:", e)
        return False

def display_status(temp, humidity):
    oled.fill(0)
    oled.text(f"Temp: {temp:.1f}C", 0, 0)
    oled.text(f"Humid: {humidity:.1f}%", 0, 16)
    oled.show()

def main():
    oled.fill(0)
    oled.text("IoT Monitor", 0, 0)
    oled.text("Booting...", 0, 16)
    oled.show()
    print("IoT Monitoring...")
    print("Booting...")

    while True:
        temp, humidity = read_sensor()
        if temp is None or humidity is None:
            print("Failed to read sensor data. Retrying...")
            time.sleep(2)
            continue

        send_success = send_to_thingspeak(temp, humidity)
        display_status(temp, humidity)
        print(temp, humidity)

        
        print(f"Waiting {CHECK_INTERVAL} seconds")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()