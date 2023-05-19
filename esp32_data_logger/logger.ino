#include <SD.h>
#include "Adafruit_EPD.h"

#include <WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

/************************* DHT *********************************/
#include "DHT.h"
#define DHT_SENSOR_TYPE DHT_TYPE_11
#define DHTPIN A1
#define LEDpin 21
#define DHTTYPE DHT11 
DHT dht(DHTPIN, DHTTYPE);

 


/************************* WiFi Access Point *********************************/
#define WLAN_SSID      "The Morty - est Morty"
#define WLAN_PASS       "Margaritarick" 
//#define WLAN_SSID       "pd3d"
//#define WLAN_PASS       "n3w.pas."

const char *ssid = "ESPecially not your network";
const char *password = "ilovemycactus";


#define MQTT_SERVER     "192.168.0.15"                 // URL to the RPi running MQTT
#define MQTT_SERVERPORT 1883                              // MQTT service port
#define MQTT_USERNAME   ""
#define MQTT_PASSWORD   ""

/************************* DEEP Sleep Setup *********************************/

#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  5 //secs         /* Time ESP32 will go to sleep (in seconds) */

#ifdef ESP32
  #define SD_CS       14
  #define SRAM_CS     32
  #define EPD_CS      15
  #define EPD_DC      33  
#endif


#define EPD_RESET   -1 // can set to -1 and share with microcontroller Reset!
#define EPD_BUSY    -1 // can set to -1 to not use a pin (will wait a fixed delay)


Adafruit_IL0373 epd(212, 104 ,EPD_DC, EPD_RESET, EPD_CS, SRAM_CS, EPD_BUSY);


RTC_DATA_ATTR int bootCount = 0;

// Create an ESP-32 WiFiClient class to connect to the MQTT server.
WiFiClient client;
// or... use WiFiFlientSecure for SSL
//WiFiClientSecure client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt( &client, MQTT_SERVER, MQTT_SERVERPORT );

/****************************** Feeds ***************************************/

Adafruit_MQTT_Publish   soil1   = Adafruit_MQTT_Publish( &mqtt, "/feeds/soil_sensor1/message" );
Adafruit_MQTT_Publish   soil2   = Adafruit_MQTT_Publish( &mqtt, "/feeds/soil_sensor2/message" );
Adafruit_MQTT_Publish   soil3   = Adafruit_MQTT_Publish( &mqtt, "/feeds/soil_sensor3/message" );

Adafruit_MQTT_Publish   soil_val1   = Adafruit_MQTT_Publish( &mqtt, "/feeds/soil_sensor1/sensor_val" );
Adafruit_MQTT_Publish   soil_val2   = Adafruit_MQTT_Publish( &mqtt, "/feeds/soil_sensor2/sensor_val" );
Adafruit_MQTT_Publish   soil_val3   = Adafruit_MQTT_Publish( &mqtt, "/feeds/soil_sensor3/sensor_val" );

Adafruit_MQTT_Publish   temperture  = Adafruit_MQTT_Publish( &mqtt, "/feeds/temp" );
Adafruit_MQTT_Publish   humidity   = Adafruit_MQTT_Publish( &mqtt, "/feeds/humidity" );
Adafruit_MQTT_Publish   heat_index   = Adafruit_MQTT_Publish( &mqtt, "/feeds/heat" );

Adafruit_MQTT_Publish   light   = Adafruit_MQTT_Publish( &mqtt, "/feeds/light" );

Adafruit_MQTT_Subscribe onoffbutton = Adafruit_MQTT_Subscribe( &mqtt, "/feeds/onoff" );

#include "Adafruit_seesaw.h"

Adafruit_seesaw ss;
 
float soilMoistureValue1 = 0;
float soilMoistureValue2 = 0;
float soilMoistureValue3 = 0;

void setup() {
  
  Serial.begin(115200); 
  dht.begin();
  // open serial port, set the baud rate to 9600 bps
  // Connect to WiFi access point.
  
  pinMode(LEDpin, OUTPUT);

  
  epd.begin();
  epd.setTextWrap(true);
  epd.setTextSize(1.5);
}

void loop() {
  float h = dht.readHumidity();
  float f = dht.readTemperature(true);

  int photocellPin = A2;
  int photocellReading;
  photocellReading = analogRead(photocellPin); 
  //soilMoistureValue1 = analogRead(A7);
  //soilMoistureValue2 = analogRead(A3);
  
  epd.clearBuffer();
  epd.setCursor(10, 10);
  epd.setTextColor(EPD_RED); epd.println("Current readings:");
  epd.setTextColor(EPD_BLACK); epd.print("Temperature:");epd.setTextColor(EPD_RED);epd.print(f); epd.println("");
  epd.setTextColor(EPD_BLACK); epd.print("Light:");epd.setTextColor(EPD_RED);epd.print(photocellReading);epd.println("");
  epd.setTextColor(EPD_BLACK); epd.print("Humditity:");epd.setTextColor(EPD_RED);epd.print(photocellReading);epd.println("");
  epd.setTextColor(EPD_BLACK); epd.print("Planter1: ");epd.setTextColor(EPD_RED);epd.print("454");epd.println("");
  epd.setTextColor(EPD_BLACK); epd.print("Planter2: ");epd.setTextColor(EPD_RED);epd.print("787");epd.println("");
  epd.display();
  
  
  photocellReading = analogRead(photocellPin);  
  Serial.println(photocellReading);
  
  Serial.println(soilMoistureValue1);
  Serial.println(soilMoistureValue2);
  Serial.println(soilMoistureValue3);
  

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
  
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  epd.println("WiFi connected");
  epd.display();
  MQTT_connect();

  soil_val1.publish(soilMoistureValue1);
  soil_val2.publish(soilMoistureValue2);
 
  temperture.publish(f);
  humidity.publish(h);
  heat_index.publish(hif);
  light.publish(photocellReading);

  epd.print("all data successuful published :)");
  epd.display();
  

  //First we configure the wake up source
  //We set our ESP32 to wake up every 5 seconds
 
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("Setup ESP32 to sleep for every " + String(TIME_TO_SLEEP) +
  " Seconds");
  Serial.println("Going to sleep now");
  delay(1000);
  Serial.flush(); 
  //esp_deep_sleep_start();
  Serial.println("This will never be printed"); 
  
}
void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}

void print_wakeup_reason(){
  esp_sleep_wakeup_cause_t wakeup_reason;

  wakeup_reason = esp_sleep_get_wakeup_cause();

  switch(wakeup_reason)
  {
    case ESP_SLEEP_WAKEUP_EXT0 : Serial.println("Wakeup caused by external signal using RTC_IO"); break;
    case ESP_SLEEP_WAKEUP_EXT1 : Serial.println("Wakeup caused by external signal using RTC_CNTL"); break;
    case ESP_SLEEP_WAKEUP_TIMER : Serial.println("Wakeup caused by timer"); break;
    case ESP_SLEEP_WAKEUP_TOUCHPAD : Serial.println("Wakeup caused by touchpad"); break;
    case ESP_SLEEP_WAKEUP_ULP : Serial.println("Wakeup caused by ULP program"); break;
    default : Serial.printf("Wakeup was not caused by deep sleep: %d\n",wakeup_reason); break;
  }
}
