
//  
//
//              This is Teensy 4.1 code that uses MQTT to send the Master String
//
//
//---------------------------------------------------------------------------------------------------
//
//
//              Later on in the code, specifically in the setup() and loop() part, comments 
//              mention things called "status codes". Those are specific to the PubSubClinet
//              library we are using to implement the MQTT protocol for the teensy. The status codes
//              range for -5 to 5. Here is what each of the mean: 
//                
//              
//              -4 : MQTT_CONNECTION_TIMEOUT - the server didn't respond within the keepalive time
//              -3 : MQTT_CONNECTION_LOST - the network connection was broken
//              -2 : MQTT_CONNECT_FAILED - the network connection failed
//              -1 : MQTT_DISCONNECTED - the client is disconnected cleanly
//               0 : MQTT_CONNECTED - the client is connected
//               1 : MQTT_CONNECT_BAD_PROTOCOL - the server doesn't support the requested version of MQTT
//               2 : MQTT_CONNECT_BAD_CLIENT_ID - the server rejected the client identifier
//               3 : MQTT_CONNECT_UNAVAILABLE - the server was unable to accept the connection
//               4 : MQTT_CONNECT_BAD_CREDENTIALS - the username/password were rejected
//               5 : MQTT_CONNECT_UNAUTHORIZED - the client was not authorized to connect
//
//
#include <SPI.h>
#include <TimeLib.h>
#include <NativeEthernet.h>     //Teensy 4.1 specific ethernet library
#include <PubSubClient.h>       //Teensy MQTT implementation library

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//              Ethernet set up including MAC address for Gromit
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//                                    VARIABLES USED
//                                      

byte mac[] = { 0x04, 0xe9, 0xe5, 0x0b, 0xab, 0x6c };        //MAC address for Gromit. Used to obtain an IP address from Carleton's DHCP

EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

String topic = "CarletonWeatherTower";

String input = "";                                          //legacy code
String data = "";                                           //legacy code

unsigned long timer = 0;                                    //legacy code
unsigned long previous_millis = 0;                          //legacy code

//------------------------------------------------------------------------------------------------------------

// void callback(char* topic, byte* payload, unsigned int length) {
//   // handle message arrived
// }


//setup_ethernet(): Teensy establishes an ethernet connection with LAN
//The Teensy gives its MAC address to the DHCP server and receives an IP address in return
void setup_ethernet() {
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to obtain an IP address using DHCP");
    while(true);
  }
  else { 
    Serial.println("IP address obtained");
    Serial.print("IP address is at: ");
    Serial.println(Ethernet.localIP());
  }  
}

//Choose the server to be used as a broker for communication
//Could be public for testing, or private for production
void setup_broker() {
  Serial.print("Status code before initializing to broker server: ");
  Serial.println(mqttClient.state());
  mqttClient.setServer("test.mosquitto.org", 1883);
  Serial.print("Status code after initializing to broker server: ");
  Serial.println(mqttClient.state());
}

//connects to the broker when connection is lost which occurs at random sometimes.
//After connection is successful, the string is published.
void commence_connection() {
  while (!mqttClient.connected()) { // Loop until we're reconnected
    Serial.print("Attempting MQTT connection...");
    String clientId = "TeensyClient-"; // Create a random client ID
    clientId += String(random(0xffff), HEX);
    if (mqttClient.connect(clientId.c_str())) { // Attempt to connect
      Serial.println("Connected");
      Serial.print("Status code after connecting to broker server: "); // Once connected, publish an announcement...
      Serial.println(mqttClient.state());
      // mqttClient.publish("test", "I'm publishing");
    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      delay(5000); // Wait 5 seconds before retrying
    }
  }
}

/*char* buffer_creator(String text) {
  char text_array[text.length()];
  return text.toCharArray(text_array, sizeof(text_array));
}*/

void publish_string(String topic, String data) {
  char topic_array[topic.length()* 2];
  topic.toCharArray(topic_array, sizeof(topic_array));
  char data_array[data.length() * 2];
  data.toCharArray(data_array, sizeof(data_array));
  Serial.print("Publishing Check...");
  Serial.println(mqttClient.publish(topic_array, data_array));
}

// String request_data() {} //is this necessary? how is this different from callback?

void setup() {
  Serial1.begin(9600);                            // baud rate to talk to the Arduino Mega; simulator uses 9600
  Serial.begin(57600);                             // baud rate for the teensy serial monitor
  // while (!Serial);                                // setup() commences only when serial monitor is opened. FOR TESTING PURPOSES ONLY. DELETE IN PRODUCTION.
  Serial.println("Teensy is in setup");
  delay(2000);

  setup_ethernet();
  delay(2000);
  setup_broker();                                 // The Teensy now sets which server it will use as a broker
  delay(2000);
  commence_connection();                          // The Teensy now attempts to connect to the server
}

//Sends signal to get data every 30 seconds
void loop() {
    unsigned long current_millis = millis();
    if (current_millis - previous_millis >= 30000) {     // get the data every 30 seconds
      previous_millis = current_millis;                 // reset the millisecond tracker to the current time
      Serial1.print("GD");                              // send a "GD" to the arduino to Get the Data
      Serial.println("Requesting data from the arduino");
    }
    delay(5000);

    // if (!mqttClient.connected()) {
    //   Serial.println("I'm not connected");
    //   commence_connection();
    // }

    if (Serial1.available()) {
        // mqttClient.publish("test", "received data");
        if (!mqttClient.connected()) {
        // Serial.println("I'm not connected");
          commence_connection();
        }

        data += Serial1.readString();    //checks whether or not the end of the data string sent by Arduino has been reached
        Serial.print("Data: ");
        Serial.println(data);
        Serial.println("Publication topic: " + topic);
        publish_string(topic, data);
        data = "";
    }
}
