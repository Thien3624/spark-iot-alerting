from kafka import KafkaProducer
import paho.mqtt.client as mqtt
import json, ssl, os

producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP"))

def on_message(client, userdata, msg):
    print(f"Bridge received: {msg.payload.decode()}")
    producer.send(os.getenv("KAFKA_TOPIC"), msg.payload)

mqtt_client = mqtt.Client("mqtt-kafka-bridge")
mqtt_client.username_pw_set(os.getenv("MQTT_USERNAME"), os.getenv("MQTT_PASSWORD"))
mqtt_client.tls_set(tls_version=ssl.PROTOCOL_TLS)
mqtt_client.connect(os.getenv("MQTT_BROKER"), int(os.getenv("MQTT_PORT", 8883)))

mqtt_client.subscribe(os.getenv("MQTT_TOPIC"))
mqtt_client.on_message = on_message
mqtt_client.loop_forever()
