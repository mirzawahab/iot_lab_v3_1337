# only dht data store to influxdb from esp32 via mosquitto mqtt broker

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
import time

# InfluxDB setup
INFLUXDB_URL = "http://localhost:8086"  # InfluxDB server URL
INFLUXDB_TOKEN = "rUYwHOkN3hNkwu5Qoh3wNQjg2EuwPEAz0RgBXAqmdU0cf3tc6tZwkNUf4xNsGSoRlP4k-pp72NZx8FNJfDMl-A=="  # Replace with your InfluxDB token
INFLUXDB_ORG = "iotrix"      # Replace with your InfluxDB organization name
INFLUXDB_BUCKET = "dht_esp32"  # InfluxDB bucket name

# MQTT setup
MQTT_BROKER = "192.168.181.57"  # ESP32's MQTT broker address
MQTT_PORT = 1884                # MQTT port
MQTT_TOPIC_TEMP = "esp32/dht/temp"
MQTT_TOPIC_HUM = "esp32/dht/hum"

# Create a client instance for MQTT
mqtt_client = mqtt.Client()

# InfluxDB client setup
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxdb_client.write_api()

# Flag to track if we've received temperature and humidity data
temperature = None
humidity = None

# Function to handle incoming MQTT messages
def on_message(client, userdata, msg):
    global temperature, humidity
    try:
        if msg.topic == MQTT_TOPIC_TEMP:
            temperature = float(msg.payload.decode())
            print(f"Received Temperature: {temperature}°C")
        elif msg.topic == MQTT_TOPIC_HUM:
            humidity = float(msg.payload.decode())
            print(f"Received Humidity: {humidity}%")
        
        # If both temperature and humidity are received, write to InfluxDB
        if temperature is not None and humidity is not None:
            # Create a data point for InfluxDB using the Point class
            point = Point("dht_data") \
                .tag("device", "esp32") \
                .field("temperature", temperature) \
                .field("humidity", humidity)

            # Write the data to InfluxDB
            write_api.write(bucket=INFLUXDB_BUCKET, record=point)
            print(f"Data written to InfluxDB: Temperature: {temperature}°C, Humidity: {humidity}%")

            # Reset the values to avoid duplicate writes
            temperature = None
            humidity = None
    except Exception as e:
        print(f"Error processing message: {e}")

# Function to connect to MQTT broker and subscribe to topics
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC_TEMP)
    client.subscribe(MQTT_TOPIC_HUM)

# Set up MQTT client
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop
mqtt_client.loop_start()

try:
    # Keep the program running to listen for incoming MQTT messages
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Stop the MQTT client loop
    mqtt_client.loop_stop()
    influxdb_client.close()  # Close InfluxDB client connection
