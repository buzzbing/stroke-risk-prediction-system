#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "HX711.h"

#define SERVER_IP "http://192.168.43.170:8088/test/"
#define echoPin D7
#define trigPin D8


//#ifndef STASSID
//#define STASSID "abhay_fbtwl_2.4"
//#define STAPSK  "0612204283"
//#endif

float ht;
float wt;
//#ifndef STASSID
//#define STASSID "Nupur"
//#define STAPSK  "Nupur@111"
//#endif

#ifndef STASSID
#define STASSID "RP"
#define STAPSK  "rakshya1"
#endif
const int LOADCELL_DOUT_PIN = D5;
const int LOADCELL_SCK_PIN = D6;
//const int LOADCELL_DOUT_PIN = 5;
//const int LOADCELL_SCK_PIN = 6;
HX711 scale;
 

long duration;
float distance;

float weight; 
float calibration_factor = -17580; // for me this value works just perfect 419640 
void setup() {
  Serial.begin(115200);



  
  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");
  scale.set_scale();
  scale.tare(); //Reset the scale to 0
  long zero_factor = scale.read_average(); //Get a baseline reading
  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
}
void loop() {
  scale.set_scale(calibration_factor); //Adjust to this calibration factor
  Serial.print("Reading: ");
  weight = scale.get_units(5); 
  //Serial.print(scale.get_units(), 2);
 // Serial.print(" lbs"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print("Kilogram:");
  wt = abs(weight);
  Serial.print( abs(weight)); 
  Serial.print(" Kg");
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  
  Serial.println();
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibration_factor += 10;
    else if(temp == '-' || temp == 'z')
      calibration_factor -= 10;
  }

//  if(abs(weight)>10)
//  { wt = abs(weight);}
//  else{ wt = 0;}
  
  pinMode(trigPin, OUTPUT);
digitalWrite(trigPin, LOW);
//delay(200);

digitalWrite(trigPin, HIGH);
//delay(1000);

digitalWrite(trigPin, LOW);

pinMode(echoPin, INPUT);

duration = pulseIn(echoPin, HIGH);//reads echo pin returns the wave travel time in microsecs
distance = duration * 0.034/2;//distance calculation

Serial.print("Distance: ");
float height = distance/100;
Serial.print(distance/100);
Serial.println(" m");

//if(height>0)
//{ht = height;}
//else{ht= 0;}


delay(1000);

// wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;
    
    
    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client,SERVER_IP); //HTTP
//    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    http.addHeader("Content-Type","application/json");

//    String data = "hey this is me";
    Serial.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body

//    if((ht!=0) && (wt!=0))
//    {
    String httpRequestData = "{\"height\":\"" + String(height) +"\", \"weight\":\"" + String(wt)+"\"}";

 
    int httpResponseCode = http.POST(httpRequestData);
    Serial.println(httpResponseCode);

    // httpCode will be negative on error
    if (httpResponseCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST IN... code: %d\n", httpResponseCode);

    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpResponseCode).c_str());

    }
//    }
//    else{
//      Serial.print("\nToo Low value of height or weight\n");
//    }
    http.end();
  }
//ht =0;//additional code
//wt =0;//additional code
  delay(1000);
//  delay(1000);
}
