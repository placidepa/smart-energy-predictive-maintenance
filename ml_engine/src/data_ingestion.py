import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost" # Adjust if running outside Docker host
MQTT_TOPIC = "factory/machine_1/power_metrics"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        print(f"Received metrics: V={payload.get('voltage')}, I={payload.get('current')}")
        # TODO: Route to time-series database or real-time ML inference queue
    except json.JSONDecodeError:
        print("Failed to decode JSON payload")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()