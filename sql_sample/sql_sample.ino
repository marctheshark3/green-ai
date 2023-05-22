#include <SQLite3.h>

SQLite3 db;

void setup() {
  // Connect to Wi-Fi and initialize the sensor

  if (!db.open("sensor_data.db")) {
    Serial.println("Failed to open database");
    while (1);
  }

  // Create the 'sensor_data' table if it doesn't exist
  if (!db.exec("CREATE TABLE IF NOT EXISTS sensor_data (temperature REAL, humidity REAL)")) {
    Serial.println("Failed to create table");
    while (1);
  }
}

void loop() {
  // Read temperature and humidity from sensor

  // Stream the data to the database
  String query = "INSERT INTO sensor_data (temperature, humidity) VALUES (";
  query += temperature;
  query += ", ";
  query += humidity;
  query += ")";

  if (!db.exec(query)) {
    Serial.println("Failed to insert data");
    while (1);
  }

  delay(30000); // Wait for 30 seconds between readings
}
