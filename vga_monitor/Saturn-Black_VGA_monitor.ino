/*
*******************************************************************************
* Author: Robert MacH
* Describe: Change colour based on location, sourced from MQTT
* Date: 2024/05/16
*******************************************************************************
*/
#include "M5Core2.h"
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);

// Configure the name and password of the connected wifi and your MQTT Serve
// host. 
const char* ssid        = "infrastructure";
const char* password    = "4QKQXBKXkXsT";
const char* mqtt_server = "csse4011-iot.zones.eait.uq.edu.au";

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
int value = 1;
int retries = 0;

//MQTT Functions
void mqttSetup();
void callback(char* topic, byte* payload, unsigned int length);

//Wifi Functions
void setupWifi();
void reConnect();

//Screen Colour functions
void setColour(int location);


void mqttSetup(){
  M5.begin();
  setupWifi();
  client.setServer(mqtt_server, 1883);  // Sets the server details.
  client.setCallback(callback);  // Sets the message callback function.
}

void setup() {
    mqttSetup();
}


void loop() {
    if (!client.connected()) {
        reConnect();
    }

    client.loop();  
    // This function is called periodically to allow clients to
    // process incoming messages and maintain connections to the
    // server.
    float distance = 0;

    unsigned long now = millis();  // Obtain the host startup duration.  获取主机开机时长
    if (now - lastMsg > 200) {
        if (value % 24 == 0) {
            M5.Lcd.clear();
            M5.Lcd.setCursor(0, 0);
        }

        lastMsg = now;
    }
     
}

void setupWifi() {
    delay(10);
    M5.Lcd.printf("Connecting to %s", ssid);
    WiFi.mode(
        WIFI_STA);  // Set the mode to WiFi station mode.  设置模式为WIFI站模式
    WiFi.begin(ssid, password);  // Start Wifi connection.  开始wifi连接

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        M5.Lcd.print(".");
    }
    M5.Lcd.printf("\nSuccess\n");
}

void setColour(int location){
  if (location > 20){
    location = -1;
  }

  M5.Lcd.fillScreen((uint16_t) ((((float)0xFFFF)/20) * (location <= 20 && location >= 0 ? location : 0)));

  M5.Lcd.setTextSize(2);
  M5.Lcd.setCursor(0, 0);

  switch(location){
    case 0:
      M5.Lcd.print("L2 West Dead End");
      break;
    case 1:
      M5.Lcd.print("L2 Stairwell West");
      break;
    case 2:
      M5.Lcd.print("L2 Common Area West");
      break;
    case 3:
      M5.Lcd.print("L2 Command Area North");
      break;
    case 4:
      M5.Lcd.print("L2 Common Area East");
      break;
    case 5:
      M5.Lcd.print("L2 Entry West");
      break;
    case 6:
      M5.Lcd.print("L2 Entry East");
      break;
    case 7:
      M5.Lcd.print("L2 Elevators");
      break;
    case 8:
      M5.Lcd.print("L2 Corridor West");
      break;
    case 9:
      M5.Lcd.print("L2 Corridor Centre");
      break;
    case 10:
      M5.Lcd.print("L2 Corridor East");
      break;
    case 11:
      M5.Lcd.print("L2 Stairwell East");
      break;
    case 12:
      M5.Lcd.print("L1 West Dead End");
      break;
    case 13:
      M5.Lcd.print("L1 Stairwell West");
      break;
    case 14:
      M5.Lcd.print("L1 Entry Lower");
      break;
    case 15:
      M5.Lcd.print("L1 Entry Upper");
      break;
    case 16:
      M5.Lcd.print("L1 Elevator");
      break;
    case 17:
      M5.Lcd.print("L1 Corridor West");
      break;
    case 18:
      M5.Lcd.print("L1 Corridor Centre");
      break;
    case 19:
      M5.Lcd.print("L1 Stairwell East");
      break;
    case 20:
      M5.Lcd.print("L1 Hallway East");
      break;
    case 21:
      M5.Lcd.print("L2 West Dead End");
      break;
    default:
      M5.Lcd.print("Invalid Location ID");
      break;
  }
  return;
}

void callback(char* topic, byte* payload, unsigned int length) {

    char command[20];

    for (int i = 0; i < length; i++) {
      if(length > 20){
        M5.Lcd.println("Command too Long! Len = ");
        M5.Lcd.print(length);
        break;
      }
      command[i] = ((char)payload[i]);
      M5.Lcd.print((char)payload[i]);
    }

    M5.Lcd.print("Message arrived [");
    M5.Lcd.print(topic);
    M5.Lcd.print("] ");

    for (int i = 0; i < length; i++) {
      M5.Lcd.print((char)payload[i]);
    }

    setColour(atoi(command));

    M5.Lcd.println();
}

void reConnect() {
    while (!client.connected()) {
        M5.Lcd.print("Attempting MQTT connection...");
        // Create a random client ID.  创建一个随机的客户端ID
        String clientId = "M5Stack-";
        clientId += String(random(0xffff), HEX);
        // Attempt to connect.
        if (client.connect(clientId.c_str())) {
            M5.Lcd.printf("\nSuccess\n");
            M5.Lcd.println("Awaiting first message");
            // Once connected, publish an announcement to the topic.
            client.publish("local44333289", "VGA Monitor Online");
            // ... and resubscribe.
            client.subscribe("local44333289");
        } else {
            M5.Lcd.print("failed, rc=");
            M5.Lcd.print(client.state());
            M5.Lcd.println("try again in 5 seconds");
            delay(5000);
            retries++;
        }
        if (retries > 10){
          M5.Lcd.clear();
          retries = 0;
          M5.Lcd.setCursor(0,0);
        }
    }
}
