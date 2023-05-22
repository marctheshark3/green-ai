#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

/************************* DHT Sensor *********************************/
#define DHT_PIN A0      // Pin connected to the DHT sensor
#define DHT_TYPE DHT11 // DHT sensor type (DHT11 or DHT22)
DHT dht(DHT_PIN, DHT_TYPE);

/************************* Wi-Fi and MQTT Settings *********************************/
const char* ssid = "PikesPeakHighFi";
const char* password = "scubamailloux";
const char* mqttServer = "192.168.1.81";

#define MQTT_SERVER "192.168.1.81"                 // URL to the RPi running MQTT
#define MQTT_SERVERPORT 1883                              // MQTT service port
const int mqttPort = 1883;
const char* mqttUsername = "marctheshark";  // MQTT broker username (if required)
const char* mqttPassword = "cactuslife43ver";  // MQTT broker password (if required)
const char* temperatureTopic = "/feeds/sensor_a/temp";
const char* humidityTopic = "/feeds/sensor_a/humidity";
const char* heatTopic = "/feeds/sensor_a/heat";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  //WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected to Wi-Fi");

  // Connect to MQTT broker
  mqttClient.setServer(MQTT_SERVER, MQTT_SERVERPORT);
  // Uncomment the following line if you need to provide MQTT broker credentials
  // mqttClient.setCredentials(mqttUsername, mqttPassword);
  
  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  // Check if connected to MQTT broker, reconnect if necessary
  if (!mqttClient.connected()) {
    reconnect();
  }

  // Read temperature and humidity from DHT sensor
  float temperature = dht.readTemperature(true);
  float humidity = dht.readHumidity();
  float heat_index = dht.computeHeatIndex(temperature, humidity);

  // Publish ctemperature and humidity data to MQTT topics
  publishData(temperatureTopic, temperature);
  publishData(humidityTopic, humidity);
  publishData(heatTopic, heat_index);

  delay(10000); // Publish data every 30 seconds
}

void reconnect() {
  // Loop until connected to MQTT broker
  while (!mqttClient.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (mqttClient.connect("ESP32Client")) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect to MQTT broker, retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void publishData(const char* topic, float data) {
  // Convert float to string
  char dataStr[10];
  sprintf(dataStr, "%.2f", data);

  // Publish data to MQTT topic
  if (mqttClient.publish(topic, dataStr)) {
    Serial.print("Published to ");
    Serial.print(topic);
    Serial.print(": ");
    Serial.println(dataStr);
  } else {
    Serial.println("Failed to publish data");
  }
}
