//#include <SD.h>
#include "Adafruit_EPD.h"

//#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

/************************* DHT *********************************/
#include "DHT.h"
#define DHT_SENSOR_TYPE DHT_TYPE_11
#define DHTPIN A0
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  
  Serial.begin(115200); 
  dht.begin();
  // open serial port, set the baud rate to 9600 bps
  // Connect to WiFi access point.
  /*
  pinMode(LEDpin, OUTPUT);

  
  epd.begin();
  epd.setTextWrap(true);
  epd.setTextSize(1.5);
  */
}

void loop() {
  float h = dht.readHumidity();
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  float hif = dht.computeHeatIndex(f, h);
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));

  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hif);
  Serial.println(F("°F"));

  delay(5000);
  

  
}
