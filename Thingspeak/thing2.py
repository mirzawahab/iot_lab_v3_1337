import machine
import dht
import urequests
import time
import ujson
from machine import Pin, SoftI2C
import ssd1306

# Configuration
THINGSPEAK_API_KEY = "9ECTMWHIW9662T3N"
THINGSPEAK_WRITE_URL = "https://api.thingspeak.com/update"

THINGSPEAK_READ_API_KEY = "W18P1YIO3RJXGM3K"
THINGSPEAK_ALERTS_URL = "https://api.thingspeak.com/channels/2923687/feeds/last.json"

DHT_PIN = 4
CHECK_INTERVAL = 2

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
    
def get_thingspeak_alerts():
    try:
        url = f"{THINGSPEAK_ALERTS_URL}?api_key={THINGSPEAK_READ_API_KEY}"
        response = urequests.get(url)
        data = ujson.loads(response.text)
        response.close()
        alert = data.get('field3', None)
        return alert if alert and alert != "0" else None
    except Exception as e:
        print("ThingSpeak alert fetch error:", e)
        return None

def display_status(temp, humidity, alert=None):
    oled.fill(0)
    oled.text(f"Temp: {temp:.1f}C", 0, 0)
    oled.text(f"Humid: {humidity:.1f}%", 0, 16)
    if alert:
        oled.text("ALERT:", 0, 48)
        oled.text(alert[:16], 0, 56)
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
        if send_success:
            alert = get_thingspeak_alerts()


        display_status(temp, humidity,alert)
        print(temp, humidity)
        print(alert)

        
        print(f"Waiting {CHECK_INTERVAL} seconds")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()