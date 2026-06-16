#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "192.168.1.100"; // Replace with your Edge Gateway/Computer IP

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
    delay(10);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
}

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
}

void loop() {
    if (!client.connected()) { 
        // TODO: Add reconnection logic 
    }
    client.loop();

    // TODO: Read hardware sensors (e.g., PZEM-004T or CT/PT)
    float voltage = 230.0; 
    float current = 10.5;
    
    // TODO: Format as JSON and publish to "factory/machine_1/power_metrics"
    
    delay(1000); 
}