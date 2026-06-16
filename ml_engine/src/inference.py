import json
import torch
import paho.mqtt.client as mqtt
from model import AnomalyAutoencoder
from preprocess import TimeSeriesPreprocessor

MQTT_BROKER = "localhost"
TOPIC_IN = "factory/machine_1/power_metrics"
TOPIC_OUT = "factory/machine_1/anomaly_alerts"
THRESHOLD = 0.05 # MSE limit before triggering a fault

model = AnomalyAutoencoder()
model.eval() # Set to evaluation mode
preprocessor = TimeSeriesPreprocessor(window_size=60)
mqtt_client = mqtt.Client()

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    window = preprocessor.add_reading(payload['voltage'], payload['current'], payload['power'])
    
    if window is not None:
        tensor_data = torch.tensor(window, dtype=torch.float32).unsqueeze(0)
        
        with torch.no_grad():
            reconstruction = model(tensor_data)
            mse_loss = torch.mean((tensor_data - reconstruction) ** 2).item()
            
            is_fault = mse_loss > THRESHOLD
            alert_payload = json.dumps({"mse_loss": mse_loss, "fault_detected": is_fault})
            client.publish(TOPIC_OUT, alert_payload)
            
            if is_fault:
                print(f"⚠️ FAULT DETECTED! Loss: {mse_loss:.4f}")

mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.subscribe(TOPIC_IN)
mqtt_client.loop_forever()