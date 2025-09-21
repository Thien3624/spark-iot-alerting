import paho.mqtt.client as mqtt
import random, time, json, ssl, os

broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
topic = os.getenv("MQTT_TOPIC")
username = os.getenv("MQTT_USERNAME")
password = os.getenv("MQTT_PASSWORD")

client = mqtt.Client("temp-simulator")
client.username_pw_set(username, password)
client.tls_set(tls_version=ssl.PROTOCOL_TLS) 

client.connect(broker, port)

while True:
    temp = random.uniform(20, 50)
    msg = json.dumps({"temperature": temp})
    client.publish(topic, msg)
    print(f"Published: {msg}")
    time.sleep(2)
