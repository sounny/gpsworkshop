/* 
  GPS Workshop - Arduino IoT Cloud Version
  ISU MSS26
  
  This sketch reads GPS data from a NEO-6M module and sends it to Arduino IoT Cloud.
  
  Wiring:
    GPS TX  -> Arduino Pin 0 (RX)
    GPS RX  -> Arduino Pin 1 (TX)
    GPS VCC -> Arduino 5V
    GPS GND -> Arduino GND
*/

  // Arduino IoT Cloud Variables:
  //   float latitude;      - GPS latitude in decimal degrees
  //   float longitude;     - GPS longitude in decimal degrees
  //   float altitude;      - Altitude in meters
  //   int satellites;      - Number of satellites in view
  //   String gps_time;     - Current UTC time from GPS

/* 
  GPS Workshop - Arduino IoT Cloud Version
  Config: Hardware Serial1 on Pins 0 & 1
*/

#include "thingProperties.h"
#include <TinyGPS++.h>

// The TinyGPS++ object
TinyGPSPlus gps;

// Timer for GPS updates (don't flood the cloud)
unsigned long lastUpdate = 0;
const unsigned long UPDATE_INTERVAL = 2000; // Update every 2 seconds

void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  delay(1500); 

  // Start the Hardware Serial port for the GPS (Pins 0 and 1)
  // Note: On Uno R4 WiFi, Serial1 is Pins 0/1
  Serial1.begin(9600);

  Serial.println(F("===================================="));
  Serial.println(F("  GPS Workshop - IoT Cloud Version"));
  Serial.println(F("  Config: Hardware Serial1 on Pins 0 & 1"));
  Serial.println(F("===================================="));
  Serial.println();

  // Defined in thingProperties.h
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
  
  Serial.println(F("Searching for GPS satellites..."));
}

void loop() {
  ArduinoCloud.update();
  
  // Read data from the GPS module on Serial1
  while (Serial1.available() > 0) {
    char c = Serial1.read();
    if (gps.encode(c)) {
      if (millis() - lastUpdate >= UPDATE_INTERVAL) {
        updateGPSData();
        lastUpdate = millis();
      }
    }
  }

  // DIAGNOSTIC LOOP
  if (millis() > 5000 && millis() - lastUpdate > 5000) {
    if (gps.charsProcessed() < 10) {
      Serial.println(F("ERROR: No GPS data received! Check wiring."));
      Serial.println(F("       GPS TX -> Arduino Pin 0"));
      Serial.println(F("       GPS RX -> Arduino Pin 1"));
    } else if (gps.sentencesWithFix() == 0) {
      Serial.print(F("DIAGNOSTIC: connected ("));
      Serial.print(gps.charsProcessed());
      Serial.println(F(" bytes). Waiting for fix..."));
    }
    lastUpdate = millis();
  }
}

void updateGPSData() {
  // Update Location
  if (gps.location.isValid()) {
    latitude = gps.location.lat();
    longitude = gps.location.lng();
    
    Serial.print(F("Location: "));
    Serial.print(latitude, 6);
    Serial.print(F(", "));
    Serial.println(longitude, 6);
  } else {
    Serial.println(F("Location: Searching for satellites..."));
  }

  // Update Altitude
  if (gps.altitude.isValid()) {
    altitude = gps.altitude.meters();
    Serial.print(F("Altitude: "));
    Serial.print(altitude);
    Serial.println(F(" m"));
  }

  // Update Satellites
  satellites = gps.satellites.value();
  Serial.print(F("Satellites: "));
  Serial.println(satellites);

  // Update Time
  if (gps.time.isValid()) {
    char timeBuffer[20];
    sprintf(timeBuffer, "%02d:%02d:%02d UTC", 
            gps.time.hour(), 
            gps.time.minute(), 
            gps.time.second());
    gps_time = String(timeBuffer);
    Serial.print(F("Time: "));
    Serial.println(gps_time);
  }

  Serial.println(F("----------------------------------------"));
  Serial.println();
}

/*
  Since Latitude is READ_WRITE variable, onLatitudeChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onLatitudeChange() {
  // This variable is primarily written TO the cloud from GPS
  // but this callback exists if you need to respond to cloud changes
}

/*
  Since Longitude is READ_WRITE variable, onLongitudeChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onLongitudeChange() {
  // This variable is primarily written TO the cloud from GPS
}

/*
  Since Satellites is READ_WRITE variable, onSatellitesChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onSatellitesChange() {
  // This variable is primarily written TO the cloud from GPS
}

/*
  Since Altitude is READ_WRITE variable, onAltitudeChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAltitudeChange() {
  // This variable is primarily written TO the cloud from GPS
}

/*
  Since GpsTime is READ_WRITE variable, onGpsTimeChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onGpsTimeChange() {
  // This variable is primarily written TO the cloud from GPS
}
