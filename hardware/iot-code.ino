#include <ESP8266WiFi.h>
#include "secrets.h"
#include "ThingSpeak.h"

#include <Wire.h>
#include <DFRobot_MAX30102.h>
#include <OneWire.h>
#include <DallasTemperature.h>

DFRobot_MAX30102 particleSensor;

#define ONE_WIRE_BUS D3
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int32_t SPO2;
int8_t SPO2Valid;
int32_t heartRate;
int8_t heartRateValid;

WiFiClient client;
String myStatus = "";

void setup() {
  Serial.begin(115200);

  // Initialize MAX30102
  if (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found. Check connections.");
    while (1);
  }

  particleSensor.sensorConfiguration(
    50,
    SAMPLEAVG_4,
    MODE_MULTILED,
    SAMPLERATE_100,
    PULSEWIDTH_411,
    ADCRANGE_16384
  );

  sensors.begin();

  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);
}

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.print("Connecting to WiFi");
  WiFi.begin(SECRET_SSID, SECRET_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(5000);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected.");
}

void loop() {

  connectWiFi();

  // Read Heart Rate & SpO2
  particleSensor.heartrateAndOxygenSaturation(
    &SPO2,
    &SPO2Valid,
    &heartRate,
    &heartRateValid
  );

  // Read Temperature
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);

  Serial.print("Heart Rate: ");
  Serial.println(heartRate);

  Serial.print("SpO2: ");
  Serial.println(SPO2);

  Serial.print("Temperature: ");
  Serial.println(tempC);

  // Send data to ThingSpeak
  ThingSpeak.setField(1, heartRate);
  ThingSpeak.setField(2, SPO2);
  ThingSpeak.setField(3, tempC);

  int response = ThingSpeak.writeFields(
    SECRET_CH_ID,
    SECRET_WRITE_APIKEY
  );

  if (response == 200) {
    Serial.println("ThingSpeak update successful.");
  } else {
    Serial.print("Error code: ");
    Serial.println(response);
  }

  delay(16000); // ThingSpeak minimum interval
}