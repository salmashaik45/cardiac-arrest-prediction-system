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

char ssid[] = "Redmi13C";     
char pass[] = "salma@4505";   
int keyIndex = 0;         
WiFiClient  client;

unsigned long myChannelNumber = 3017666;
const char * myWriteAPIKey = "GF8053OVJNAFFLJ6";

String myStatus = "";

void setup() {
  Serial.begin(115200); 
  

  if (!particleSensor.begin()) {
    Serial.println("MAX30102 was not found. Please check the connections.");
    while (1);
  }


  particleSensor.sensorConfiguration(50, SAMPLEAVG_4, MODE_MULTILED, SAMPLERATE_100, PULSEWIDTH_411, ADCRANGE_16384);

  sensors.begin();

  
  while (!Serial) {
    ; 
  }
  
  WiFi.mode(WIFI_STA); 
  ThingSpeak.begin(client);  
}

void loop() {

  particleSensor.heartrateAndOxygenSaturation(&SPO2, &SPO2Valid, &heartRate, &heartRateValid);

  Serial.print("IR=");
  Serial.print(particleSensor.getIR());
  Serial.print(" heartRate=");
  Serial.print(heartRate, DEC);
  Serial.print(" heartRateValid=");
  Serial.print(heartRateValid, DEC);
  Serial.print(" SPO2=");
  Serial.print(SPO2, DEC);
  Serial.print(" SPO2Valid=");
  Serial.println(SPO2Valid, DEC);

  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);

  Serial.print("Temperature: ");
  Serial.print(tempC);
  Serial.println(" C");

  
  if(WiFi.status() != WL_CONNECTED){
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(SECRET_SSID);
    while(WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid, pass); 
      Serial.print(".");
      delay(5000);     
    } 
    Serial.println("\nConnected.");
  }

  ThingSpeak.setField(1, heartRate);
  ThingSpeak.setField(2, SPO2);
  ThingSpeak.setField(3, tempC);

  ThingSpeak.setStatus(myStatus);
  
  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
  if(x == 200){
    Serial.println("Channel update successful.");
  }
  else{
    Serial.println("Problem updating channel. HTTP error code " + String(x));
  }
   
  delay(16000);
}