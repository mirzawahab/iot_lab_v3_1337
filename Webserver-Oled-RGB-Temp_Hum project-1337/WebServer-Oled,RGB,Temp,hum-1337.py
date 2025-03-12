import network
import socket
import time
import neopixel
import machine
from machine import Pin, I2C
from dht import DHT11
from ssd1306 import SSD1306_I2C

# WiFi Configuration
SSID = "Mirza Wahab 1"
PASSWORD = "wahab973"
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

# Wait for WiFi to connect
while not sta.isconnected():
    time.sleep(1)
    print("Connecting...")

print("Connected! IP Address:", sta.ifconfig()[0])

# NeoPixel LED Setup
np = neopixel.NeoPixel(Pin(48), 1)  # Change Pin if necessary

def set_neopixel(r, g, b):
    """ Set NeoPixel color with RGB values """
    np[0] = (r, g, b)
    np.write()

# OLED Display Setup
i2c = I2C(1, scl=Pin(9), sda=Pin(8))  # Change if necessary
oled = SSD1306_I2C(128, 64, i2c)

def display_text(text):
    """ Display text on the OLED screen """
    oled.fill(0)  # Clear screen
    oled.text(text, 0, 10)
    oled.show()

# DHT11 Sensor Setup
dht_sensor = DHT11(Pin(4))  # Change Pin if necessary

def get_sensor_data():
    """ Read temperature and humidity from DHT11 """
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        return temp, hum
    except Exception as e:
        print("DHT11 error:", e)
        return None, None

# Web Page HTML
def web_page():
    """ Generate HTML web page for ESP32 control """
    temp, hum = get_sensor_data()
    temp = temp if temp is not None else "N/A"
    hum = hum if hum is not None else "N/A"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Web Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            /* General Styles */
            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                overflow-y: auto;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
                text-align: center;
                backdrop-filter: blur(10px);
                max-width: 500px;
                width: 100%;
                margin-bottom: 20px;
            }}
            h2 {{
                margin-bottom: 20px;
                font-size: 24px;
                color: #ff6b6b; /* Red heading */
            }}
            h3 {{
                color: #4ecdc4; /* Cyan heading */
                margin-top: 20px;
                margin-bottom: 10px;
            }}

            /* RGB Sliders */
            .color-picker {{
                margin: 20px 0;
            }}
            .color-picker input[type="range"] {{
                width: 100%;
                margin: 10px 0;
                -webkit-appearance: none;
                appearance: none;
                height: 10px;
                background: #ddd;
                outline: none;
                border-radius: 5px;
                opacity: 0.7;
                transition: opacity 0.2s;
            }}
            .color-picker input[type="range"]:hover {{
                opacity: 1;
            }}
            .color-picker input[type="range"]::-webkit-slider-thumb {{
                -webkit-appearance: none;
                appearance: none;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                cursor: pointer;
            }}
            #red::-webkit-slider-thumb {{
                background: #ff6b6b; /* Red */
            }}
            #green::-webkit-slider-thumb {{
                background: #4ecdc4; /* Green */
            }}
            #blue::-webkit-slider-thumb {{
                background: #556270; /* Blue */
            }}

            /* Color Preview */
            .color-preview {{
                width: 100px;
                height: 100px;
                margin: 20px auto;
                border-radius: 10px;
                background: rgb(0, 0, 0);
                border: 2px solid #fff;
            }}

            /* Color Combination Button */
            .combination-button {{
                margin: 10px 0;
                padding: 10px;
                width: 100%;
                border: none;
                border-radius: 5px;
                background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #556270);
                color: white;
                cursor: pointer;
                transition: background 0.3s ease;
            }}
            .combination-button:hover {{
                background: linear-gradient(90deg, #556270, #ff6b6b, #4ecdc4);
            }}

            /* Gauges */
            .gauge {{
                position: relative;
                width: 150px;
                height: 150px;
                margin: 20px auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                border: 5px solid rgba(255, 255, 255, 0.2);
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.2), -5px -5px 10px rgba(255, 255, 255, 0.1);
            }}
            .gauge.temperature {{
                border-color: #ff6b6b; /* Red border */
            }}
            .gauge.humidity {{
                border-color: #4ecdc4; /* Cyan border */
            }}
            .gauge .needle {{
                position: absolute;
                width: 2px;
                height: 50%;
                background: #ff6b6b;
                bottom: 50%;
                left: 50%;
                transform-origin: bottom;
                transform: rotate(-90deg);
                transition: transform 0.5s ease;
            }}
            .gauge .needle.humidity {{
                background: #4ecdc4;
            }}
            .gauge .value {{
                position: absolute;
                top: 60%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 20px;
                color: #fff;
                cursor: pointer;
            }}
            .gauge .label {{
                position: absolute;
                bottom: -20px;
                left: 50%;
                transform: translateX(-50%);
                font-size: 14px;
                color: #fff;
                cursor: pointer;
            }}

            /* Details Card */
            .details-card {{
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                display: none; /* Hidden by default */
            }}
            .details-card ul {{
                list-style: none;
                padding: 0;
            }}
            .details-card ul li {{
                margin: 10px 0;
                font-size: 16px;
            }}

            /* Text Box */
            .text-box {{
                margin: 10px 0;
                padding: 10px;
                width: 100%;
                border: none;
                border-radius: 5px;
                background: rgba(255, 255, 255, 0.8);
                color: #333;
                font-size: 16px;
                transition: box-shadow 0.3s ease;
            }}
            .text-box:hover {{
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5);
            }}

            /* Display Button */
            .submit-button {{
                margin: 10px 0;
                padding: 10px;
                width: 100%;
                border: none;
                border-radius: 5px;
                background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #556270);
                background-size: 200% 100%;
                color: white;
                cursor: pointer;
                transition: background-position 0.5s ease;
            }}
            .submit-button:hover {{
                background-position: 100% 0;
            }}

            /* Responsive Design */
            @media (max-width: 600px) {{
                .container {{
                    padding: 20px;
                }}
                .gauge {{
                    width: 120px;
                    height: 120px;
                }}
                .gauge .value {{
                    font-size: 18px;
                }}
                .gauge .label {{
                    font-size: 12px;
                }}
                h2 {{
                    font-size: 20px;
                }}
                h3 {{
                    font-size: 16px;
                }}
                .text-box {{
                    font-size: 14px;
                }}
                .submit-button {{
                    font-size: 14px;
                }}
            }}
        </style>
        <script>
            let colorInterval = null;

            function updateSensorData() {{
                fetch('/sensor')
                    .then(response => response.json())
                    .then(data => {{
                        // Update temperature and humidity values
                        document.getElementById('temp-value').innerText = data.temp + "°C";
                        document.getElementById('hum-value').innerText = data.hum + "%";
                        
                        // Update gauge needles
                        const tempNeedle = document.getElementById('temp-needle');
                        const humNeedle = document.getElementById('hum-needle');
                        const tempAngle = (data.temp / 50) * 180 - 90; // Scale temperature to 0-50°C
                        const humAngle = (data.hum / 100) * 180 - 90; // Scale humidity to 0-100%
                        tempNeedle.style.transform = `rotate(${{tempAngle}}deg)`;
                        humNeedle.style.transform = `rotate(${{humAngle}}deg)`;
                    }})
                    .catch(error => console.error('Error fetching sensor data:', error));
            }}

            function updateColor() {{
                const r = document.getElementById('red').value;
                const g = document.getElementById('green').value;
                const b = document.getElementById('blue').value;
                
                // Update color preview
                document.getElementById('color-preview').style.backgroundColor = `rgb(${{r}}, ${{g}}, ${{b}})`;
                
                // Send color to ESP32
                fetch(`/?r=${{r}}&g=${{g}}&b=${{b}}`);
            }}

            function startColorCombination() {{
                if (colorInterval) {{
                    clearInterval(colorInterval);
                    colorInterval = null;
                    return;
                }}

                let r = 0, g = 0, b = 0;
                colorInterval = setInterval(() => {{
                    r = (r + 5) % 256;
                    g = (g + 10) % 256;
                    b = (b + 15) % 256;
                    
                    document.getElementById('red').value = r;
                    document.getElementById('green').value = g;
                    document.getElementById('blue').value = b;
                    updateColor();
                }}, 200); // Change colors every 200ms
            }}

            function showDetails(type) {{
                const tempCard = document.getElementById('temp-details');
                const humCard = document.getElementById('hum-details');
                
                if (type === 'temp') {{
                    tempCard.style.display = 'block';
                    humCard.style.display = 'none';
                }} else if (type === 'hum') {{
                    tempCard.style.display = 'none';
                    humCard.style.display = 'block';
                }}
            }}

            setInterval(updateSensorData, 2000); // Update sensor data every 2 seconds
        </script>
    </head>
    <body>
        <div class="container">
            <h2>ESP32 Web Control</h2>
            
            <h3>RGB Color Picker</h3>
            <div class="color-picker">
                <label for="red">Red:</label>
                <input type="range" id="red" min="0" max="255" value="0" oninput="updateColor()">
                
                <label for="green">Green:</label>
                <input type="range" id="green" min="0" max="255" value="0" oninput="updateColor()">
                
                <label for="blue">Blue:</label>
                <input type="range" id="blue" min="0" max="255" value="0" oninput="updateColor()">
            </div>
            <div id="color-preview" class="color-preview"></div>
            <button class="combination-button" onclick="startColorCombination()">Color Combination</button>
            
            <h3>Temperature & Humidity Gauges</h3>
            <div style="display: flex; justify-content: space-around;">
                <div class="gauge temperature">
                    <div id="temp-needle" class="needle"></div>
                    <div id="temp-value" class="value" onclick="showDetails('temp')">{temp}°C</div>
                    <div class="label" onclick="showDetails('temp')">Temperature</div>
                </div>
                <div class="gauge humidity">
                    <div id="hum-needle" class="needle humidity"></div>
                    <div id="hum-value" class="value" onclick="showDetails('hum')">{hum}%</div>
                    <div class="label" onclick="showDetails('hum')">Humidity</div>
                </div>
            </div>

            <!-- Temperature Details Card -->
            <div id="temp-details" class="details-card">
                <h3>Temperature Details</h3>
                <ul>
                    <li>Current Temperature: {temp}°C</li>
                    <li>Min Temperature: 10°C</li>
                    <li>Max Temperature: 40°C</li>
                </ul>
            </div>

            <!-- Humidity Details Card -->
            <div id="hum-details" class="details-card">
                <h3>Humidity Details</h3>
                <ul>
                    <li>Current Humidity: {hum}%</li>
                    <li>Min Humidity: 20%</li>
                    <li>Max Humidity: 80%</li>
                </ul>
            </div>
            
            <h3>Display Text on OLED</h3>
            <form action="/" method="GET">
                <input type="text" name="msg" placeholder="Enter text" class="text-box">
                <button type="submit" class="submit-button">Display</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

# Start Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
print("Web server started!")

# Main Server Loop
while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()
        print("Request:", request)
        
        # Handle Sensor Data Request
        if "GET /sensor" in request:
            temp, hum = get_sensor_data()
            response = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{{"temp": {temp}, "hum": {hum}}}'
            conn.send(response)
            conn.close()
            continue
        
        # Parse URL Parameters Manually
        if "GET /?" in request:
            params = request.split(" ")[1].split("?")[1].split("&")
            param_dict = {}
            for p in params:
                key_val = p.split("=")
                if len(key_val) == 2:
                    param_dict[key_val[0]] = key_val[1]
            
            # Handle RGB Input
            if "r" in param_dict and "g" in param_dict and "b" in param_dict:
                try:
                    r = int(param_dict.get("r", 0))
                    g = int(param_dict.get("g", 0))
                    b = int(param_dict.get("b", 0))
                    
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        set_neopixel(r, g, b)
                except ValueError:
                    print("Invalid RGB values received")
            
            # Handle OLED Text Input
            if "msg" in param_dict:
                msg = param_dict["msg"]
                print("Displaying on OLED:", msg)  # Debugging
                display_text(msg)
        
        response = web_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + response)
        conn.close()
    
    except Exception as e:
        print("Server error:", e)
        conn.close()