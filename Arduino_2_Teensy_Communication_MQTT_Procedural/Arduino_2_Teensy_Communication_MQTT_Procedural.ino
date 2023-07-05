
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
#include <NativeEthernetUdp.h>
#include <NativeEthernet.h>     //Teensy 4.1 specific ethernet library
#include <PubSubClient.h>       //Teensy MQTT implementation library
#include <SD.h>

#define MQTT_MAX_PACKET_SIZE 3000; // Set the maximum number of bytes that can be sent as MQTT payload. 

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//              Ethernet set up including MAC address for Gromit
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//                                    VARIABLES USED
//                                      

// byte mac[] = { 0x04, 0xe9, 0xe5, 0x0e, 0x52, 0xee };     //MAC address for Gromit. Used to obtain an IP address from Carleton's DHCP
byte mac[] = {0x04, 0xe9, 0xe5, 0x0b, 0xab, 0x6c};          //MAC address for Snowy

EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

String topic = "CarletonWeatherTower";

// NTP Servers (2 alternatives are listed. It may be possible to connect to ntp pool and not worry about which specific ip is available): 
IPAddress timeServer(129, 6, 15, 28); // time-a-g.nist.gov    NIST, Gaithersburg, Maryland
// IPAddress timeServer(132, 163, 97, 1); // time-a-wwv.nist.gov    WWV, Fort Collins, Colorado
// IPAddress timeServer(132, 163, 96, 1); // time-a-b.nist.gov    NIST, Boulder, Colorado

// const int timeZone = -6;     // Central Standard Time
// const int timeZone = -5;     // Central Daylight Time
const int timeZone = 0;         // Gives the actual accurate time. No shifting for time zones necessary.

EthernetUDP Udp;
unsigned int localPort = 8888;  // local port to listen for UDP packets
time_t timeOfLatestSync;       // Used to sync clock to NTP server if latest sync was more than 24 hrs ago. 


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
    while(true);      // we shouldn't have it loop without condition-less forever. 

  }
  else { 
    Serial.println("IP address obtained");
    Serial.print("IP address is at: ");
    Serial.println(Ethernet.localIP());
  }  
}

// Syncs clock with time from NTP server listed in VARIABLES USED.
// It attepmts to sync to the NTP server ever 24 hrs(86400 secs, 86400000 ms).
void setup_NTP() {
  Udp.begin(localPort);
  Serial.println("Waiting for time sync.");
  setSyncProvider(getNtpTime);
  timeOfLatestSync = now();
  // setSyncInterval(86400000);
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

void publish_string(String topic, String data) {
  char topic_array[topic.length()* 2];
  topic.toCharArray(topic_array, sizeof(topic_array));
  char data_array[data.length() * 2];
  data.toCharArray(data_array, sizeof(data_array));
  Serial.print("data_array: ");
  Serial.println(data_array);
  Serial.print("Publishing Check...");
  Serial.println(mqttClient.publish(topic_array, data_array));      // Returns 0 for success, 1 for fail. 
}

// Saves the input data string to an SD card as a .txt file
// ** The specificed file name should not include the file type (.txt), only the name.
// ** The "".txt" is added inside the function
void saveDataToSD(String dataString, String fileName) {
  fileName += ".txt";
  File savedData = SD.open(fileName.c_str(), FILE_WRITE);
  if (savedData) {
    savedData.println(dataString);
    savedData.close();
    Serial.println("Data saved to SD card in file: " + fileName);
  } else {
    Serial.println("error opening file:" + fileName);
  } 
}

// Reads data from the SD card from the specified file name 
// ** The parameter fileName should not include the file type, only the name of the file. 
// ** It is assumed all files on the SD card are .txt files.
// Returns void for now. Could return the string from the file or
// could return void and publish the string within this function.
void readFromSD(String fileName) {
  String returnStr = "";
  fileName += ".txt";
  File fileSD = SD.open(fileName.c_str(), FILE_READ);
  if (fileSD) {
    Serial.println("Reading from file: " + fileName);
    // read from the file until there's nothing else in it:
    while (fileSD.available()) {
    	returnStr += fileSD.readString();
    }
    fileSD.close();
  } else {
    Serial.println("error opening file: " + fileName);
  }
}

// String request_data() {} //is this necessary? how is this different from callback?

void setup() {
  Serial1.begin(57600);                         // baud rate to talk to the Arduino Mega; simulator uses 9600
  Serial.begin(9600);                           // baud rate for the teensy serial monitor
  // while (!Serial);                           // setup() commences only when serial monitor is opened. FOR TESTING PURPOSES ONLY. DELETE IN PRODUCTION.
  Serial.println("Teensy is in setup");
  delay(2000);

  Serial.print("Initializing SD card...");     
  if (!SD.begin(BUILTIN_SDCARD)) {
    Serial.println("SD initialization failed!");
    while (1);                                    // If the SD card initialization fails, the code effectively stops here. 
  }
  Serial.println("SD initialization done."); 
  delay(2000);

  setup_ethernet();
  delay(2000);
  setup_NTP();                                    // Time is now synched with NTP
  delay(2000);
  setup_broker();                                 // The Teensy now sets which server it will use as a broker
  delay(2000);
  commence_connection();                          // The Teensy now attempts to connect to the server
}

//Sends signal to get data every 30 seconds
void loop() {
    // Returns 1 or 3 if Ethernet connection is not maintained. 
    // Returns 2 or 4 if renewal/rebind successful. 0 = nothing happened/renewal was not needed.
    byte ethReturnByte = Ethernet.maintain(); 

    unsigned long current_millis = millis();
    if (current_millis - previous_millis >= 30000) {      // get the data every 30 seconds
      previous_millis = current_millis;                   // reset the millisecond tracker to the current time

      // Checks if Ethernet connection is still good(and updates IP from DHCP)
      // then syncs the time to NTP if the latest sync was more than 12 hrs ago. 
      // Maybe we should have the MQTT connection stuff inside here as well, to check for internet connection first?
      Serial.println("ethReturnByte: " + String(ethReturnByte));
      if (ethReturnByte == 2 || ethReturnByte == 4 || ethReturnByte == 0) {
        if (now() >= timeOfLatestSync + 86400000) {   // 86400000 ms = 24 hrs *also unsure if int() is necessary
          setup_NTP();
        } 
      }

      clearSerial1Buffer();       
      Serial1.print("GD");                                // send a "GD" to the arduino to Get the Data
      Serial.println("Requesting data from the arduino");
    }
    // delay(5000);       // Data seemed to be sent fine from Arduino without the delay.

    if (Serial1.available()) {
        // Need this char later on because Serial.read() sends text as ASCII decimal.
        // Setting char character = Serial.read() will "typecast" the output as a char.
        char character = 'a';

        // Loops through Serial1 buffer until 'S'(the starting char) is detected.
        // Maybe this detection code is unessary but the
        // clearSerial1Buffer doesn't always seem to work. More testing needed so we don't need both.
        while (character != 'S')  {                                   
          character = Serial1.read();       
        }

        // Records the time of when the 'S' is read
        String timeOfNewData = String(now());
        data = timeOfNewData + "\t";   

        data.concat(String(character));                         // Adds the 'S' that was detetected to the data string.        

        // Reads from Serial1, byte by byte, and adds the char that was read
        // until the terminating char '@' is read. 
        while (character != '@') {                      // ASCII code for '@' = 64
          while(Serial1.available()) {      
            character = Serial1.read();
            data.concat(String(character));
          }
        }

        // //TESTING
        // int i = 0;
        // while (i < 100) {                    
        //   while(Serial1.available()) {      
        //     character = Serial1.read();
        //     data.concat(String(character));
        //     i++;
        //   }
        // }

        // We may restructure this code using interrupts to always read from SD,
        // and interrupt every 30 seconds to request and write data to the SD card. 
        saveDataToSD(data, timeOfNewData); 
        readFromSD(timeOfNewData);

        Serial.print("Data: ");
        Serial.println(data);

        // mqttClient.publish("test", "received data");
        if (!mqttClient.connected()) {
        // Serial.println("I'm not connected");
          commence_connection();          
        }
        Serial.println("Publication topic: " + topic); 
        publish_string(topic, data);      
    }
}

// Reads all of, and therefore effectively 
// empties, the Serial1 buffer. 
void clearSerial1Buffer() {
  while (Serial1.available()) {
    Serial1.read();
  }
}


// NTP Functions
const int NTP_PACKET_SIZE = 48; // NTP time is in the first 48 bytes of message
byte packetBuffer[NTP_PACKET_SIZE]; //buffer to hold incoming & outgoing packets

time_t getNtpTime()
{
  while (Udp.parsePacket() > 0) ; // discard any previously received packets
  Serial.println("Transmit NTP Request");
  sendNTPpacket(timeServer);
  uint32_t beginWait = millis();
  while (millis() - beginWait < 1500) {
    int size = Udp.parsePacket();
    if (size >= NTP_PACKET_SIZE) {
      Serial.println("Received NTP Response");
      Udp.read(packetBuffer, NTP_PACKET_SIZE);  // read packet into the buffer
      unsigned long secsSince1900;
      // convert four bytes starting at location 40 to a long integer
      secsSince1900 =  (unsigned long)packetBuffer[40] << 24;
      secsSince1900 |= (unsigned long)packetBuffer[41] << 16;
      secsSince1900 |= (unsigned long)packetBuffer[42] << 8;
      secsSince1900 |= (unsigned long)packetBuffer[43];
      Serial.print("NUMBER: ");
      Serial.println(secsSince1900 - 2208988800UL + timeZone * SECS_PER_HOUR);
      return secsSince1900 - 2208988800UL + timeZone * SECS_PER_HOUR;
    }
  }
  Serial.println("No NTP Response :-(");
  return 0; // return 0 if unable to get the time
}

// send an NTP request to the time server at the given address
void sendNTPpacket(IPAddress &address)
{
  // set all bytes in the buffer to 0
  memset(packetBuffer, 0, NTP_PACKET_SIZE);
  // Initialize values needed to form NTP request
  // (see URL above for details on the packets)
  packetBuffer[0] = 0b11100011;   // LI, Version, Mode
  packetBuffer[1] = 0;     // Stratum, or type of clock
  packetBuffer[2] = 6;     // Polling Interval
  packetBuffer[3] = 0xEC;  // Peer Clock Precision
  // 8 bytes of zero for Root Delay & Root Dispersion
  packetBuffer[12]  = 49;
  packetBuffer[13]  = 0x4E;
  packetBuffer[14]  = 49;
  packetBuffer[15]  = 52;
  // all NTP fields have been given values, now
  // you can send a packet requesting a timestamp:                 
  Udp.beginPacket(address, 123); //NTP requests are to port 123
  Udp.write(packetBuffer, NTP_PACKET_SIZE);
  Udp.endPacket();
}


