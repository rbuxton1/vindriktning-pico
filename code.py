import os
import ssl
import time
import wifi
import socketpool
import board
import busio
import microcontroller
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import supervisor

def valid_header(d):
    headerValid = (d[0] == 0x16 and d[1] == 0x11 and d[2] == 0x0B)
    # debug
    if not headerValid:
        print("msg without header")
    return headerValid

measurements = [0, 0, 0, 0, 0]
measurement_idx = 0
last_pm2p5 = -1
last_temp = -1
last_rh = -1
last_press = -1

try:
    # Connect to stream
    uart = busio.UART(baudrate=9600, tx=board.GP12, rx=board.GP13)

    # Connect to WiFi
    print("Configuring network. . . ", end="")
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    pool = socketpool.SocketPool(wifi.radio)
    print("Connected as ", str(wifi.radio.ipv4_address))

    # MQTT Helpers
    def connect(mqtt_client, userdata, flags, rc):
        print("Connected to MQTT Broker!")
    def disconnect(mqtt_client, userdata, rc):
        print("Disconnected from MQTT Broker!")
    def subscribe(mqtt_client, userdata, topic, granted_qos):
        print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))
    def unsubscribe(mqtt_client, userdata, topic, pid):
        print("Unsubscribed from {0} with PID {1}".format(topic, pid))
    def publish(mqtt_client, userdata, topic, pid):
        print("Published {0}".format(topic))
        time.sleep(.1)
    def message(client, topic, message):
        print("New message on topic {0}: {1}".format(topic, message))

    # Set up a MiniMQTT Client
    print("Initializing MQTT. . ." , end="")
    mqtt_client = MQTT.MQTT(
        broker = os.getenv("mqtt_host"),
        username=os.getenv("mqtt_username"),
        password=os.getenv("mqtt_password"),
        socket_pool=pool,
    )

    # Connect callback handlers to mqtt_client
    mqtt_client.on_connect = connect
    mqtt_client.on_disconnect = disconnect
    mqtt_client.on_subscribe = subscribe
    mqtt_client.on_unsubscribe = unsubscribe
    mqtt_client.on_publish = publish
    mqtt_client.on_message = message

    print(" connecting to %s . . ." % mqtt_client.broker, end="")
    mqtt_client.connect()

    while True:
        data = uart.read(32)

        if data is not None:
            print("non-none data", data)
            v = valid_header(data)
            if v is True:
                measurement_idx = 0
                start_read = True
                if start_read is True and len(data) > 6:
                    pm25 = (data[5] << 8) | data[6]
                    measurements[measurement_idx] = pm25
                    if measurement_idx == 4:
                        start_read = False
                    measurement_idx = (measurement_idx + 1) % 5

                    if last_pm2p5 != measurements[0]:
                        last_pm2p5 = measurements[0]
                        print("Suspected PM2P5", last_pm2p5)
                        mqtt_client.publish(os.getenv('name') + "/pm2p5", last_pm2p5)
                    else:
                        print(measurements)
        

except Exception as e:
    print("Error:\n", str(e))
    print("Reloading supervisor in 5 seconds")
    time.sleep(5)
    supervisor.reload()