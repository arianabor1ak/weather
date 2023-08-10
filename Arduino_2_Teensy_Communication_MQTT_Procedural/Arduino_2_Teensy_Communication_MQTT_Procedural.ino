
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

// Manually changed in the PubSubClient.h file because the #define didn't seem to work.
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

// NTP Servers (2 alternatives are listed. It may be possible to connect to 
// 'ntp pool' and not worry about which specific ip address is available): 
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

  }
  else { 
    Serial.println("IP address obtained");
    Serial.print("IP address is at: ");
    Serial.println(Ethernet.localIP());
  }  
}

// Syncs clock with time from NTP server listed in VARIABLES USED.
void setup_NTP() {
  Udp.begin(localPort);
  Serial.println("Waiting for time sync.");
  setSyncProvider(getTeensy3Time);    // Set TimeLib to use the internal RTC
  time_t t = getNtpTime();
  Teensy3Clock.set(t);                // Set the RTC using NTP server
  setTime(t); 
  timeOfLatestSync = now();
  if (timeStatus()!= timeSet) {
    Serial.println("Unable to sync with the RTC");

  } else {
    Serial.println("RTC has set the system time");
  }
}

// Function for getting the time from RTC
time_t getTeensy3Time()
{
  return Teensy3Clock.get();
}

//Choose the server to be used as a broker for communication
//Could be public for testing, or private for production
void setup_broker() {
  Serial.print("Status code before initializing to broker server: ");
  Serial.println(mqttClient.state());
  mqttClient.setServer("test.mosquitto.org", 1883);  // Will be changed to a dedicated MQTT server at Carleton
  Serial.print("Status code after initializing to broker server: ");
  Serial.println(mqttClient.state());
}

//connects to the broker when connection is lost which occurs at random sometimes.
//After connection is successful, the string is published.
void commence_connection() {
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
    Serial.println(mqttClient.state());
  }
}

void publish_string(String topic, String data) {
  char topic_array[topic.length()* 2];
  topic.toCharArray(topic_array, sizeof(topic_array));
  char data_array[data.length() * 2];
  data.toCharArray(data_array, sizeof(data_array));
  Serial.print("Publishing Check...");
  Serial.println(mqttClient.publish(topic_array, data_array));      // Returns 0 for success, 1 for fail. 
}

bool setup_SD() {
  Serial.print("Initializing SD card...");     
  if (SD.begin(BUILTIN_SDCARD)) {
    Serial.println("SD initialization done.");
    return true;
  } else {
    Serial.println("SD initialization failed!.");
    return false;
  }
}

// Saves the input data string to an SD card as a .txt file inside the folder "unpublished"
// ** The specificed file name should not include the file type (.txt), only the name.
// ** The "".txt" is added inside this function
void unpublishedToSD(String dataString, String fileName) {
  String filePath = "unpublished/" + fileName + ".txt";
  File savedData = SD.open(filePath.c_str(), FILE_WRITE);
  if (savedData) {
    savedData.println(dataString);
    savedData.close();
    Serial.println("Unpublished data saved to SD card in file: " + filePath);
  } else {
    Serial.println("error opening file: " + filePath);
  } 
}

// Saves the input data string to an SD card as a .txt file inside the folder "published"
// ** Same file name specifications as unpublishedToSD() function
void publishedToSD(String dataString, String fileName) {
  String filePath = "published/" + fileName + ".txt";
  File savedData = SD.open(filePath.c_str(), FILE_WRITE);
  if (savedData) {
    savedData.println(dataString);
    savedData.close();
    Serial.println("Published data saved to SD card in file: " + filePath);
  } else {
    Serial.println("error opening file: " + filePath);
  } 
}

// Moves(copies and deletes original) one file(passed as a param) to the 
// folder named "published" and publishes the data from that file to mqtt client. 
// ** Assumes mqtt connection has been established.
// ** This function assumes sourceFile param ends in ".txt"
void processUnpublishedFile (File unpublishedFile) { 
  Serial.println("unpublishedFile name = " + String(unpublishedFile.name()));
  String destPath = "published/" + String(unpublishedFile.name());;
  File destFile = SD.open(destPath.c_str(), FILE_WRITE);
  String fileData = "";
  while (unpublishedFile.available()) {
    fileData += unpublishedFile.readString();
    destFile.println(fileData);
  }
  destFile.close();

  //publish the data from the moved file
  publish_string(topic, fileData);
  // remove the file from the unpublished folder
  String unpublishedFilePath = "unpublished/" + String(unpublishedFile.name());
  SD.remove(unpublishedFilePath.c_str());
  Serial.println("Finished moving/publishing file.");

}

// String request_data() {} //is this necessary? how is this different from callback?

void setup() {
  Serial1.begin(57600);                         // baud rate to talk to the Arduino Mega; simulator uses 9600
  Serial.begin(9600);                           // baud rate for the teensy serial monitor
  // while (!Serial);                           // setup() commences only when serial monitor is opened. FOR TESTING PURPOSES ONLY. DELETE IN PRODUCTION.
  Serial.println("Teensy is in setup");
  delay(500);

  if (!setup_SD()){                             // SD card setup
    setup_SD();                                 // Attempts SD setup again if first try failed.
  } else {
    if (!SD.exists("unpublished")) {            // Folder setup in SD card
      SD.mkdir("unpublished");
    }
    if (!SD.exists("published")) {
      SD.mkdir("published");
    }
  } 

  delay(500);
  setup_ethernet();
  delay(2000);
  setup_NTP();                          // RTC and TimeLib is now synched with NTP
  delay(1000);
  setup_broker();                       // The Teensy now sets which server it will use as a broker
  delay(2000);
  commence_connection();                // The Teensy now attempts to connect to the server
}

//Sends signal to get data every 30 seconds
void loop() {
  time_t timeOfNewData;   // var that holds the time of when data was received by the Teensy from the Arduino.
  // unsigned long current_millis = millis();
  // if (current_millis - previous_millis >= 30000) {      // get the data every 30 seconds
  //   previous_millis = current_millis;                   // reset the millisecond tracker to the current time

  //   clearSerial1Buffer();       
  //   Serial1.print("GD");                                // send a "GD" to the arduino to Get the Data
  //   Serial.println("Requesting data from the arduino");
  // }
  // delay(5000);       // Data seemed to be sent fine from Arduino without the delay.

  unsigned long millisOfRequest = millis();
  clearSerial1Buffer();       
  Serial1.print("GD");                                // send a "GD" to the arduino to Get the Data
  Serial.println("Requesting data from the arduino");
  while(!Serial1.available() && (millis() < millisOfRequest + 60000)); // && (millis() < millisOfRequest + 20000) This just waits until there is something in the serial1 buffer or 60 secs has passed with nothing in serial1 buffer.
  if (Serial1.available()) {
    // Serial.println("Serial1 is available!"); // testing
    // Need this char later on because Serial.read() sends text as ASCII decimal.
    // Setting char character = Serial.read() will "typecast" the output as a char.
    char character = 'a';

    // Loops through Serial1 buffer until 'S'(the starting char) is detected.
    // Maybe this detection code is unessary but the
    // clearSerial1Buffer doesn't always seem to work. More testing needed so we don't need both.
    while (character != 'S')  {                                   
      character = Serial1.read();       
    }
    // Serial.println("Starting char 'S' found! "); // testing

    // Records the time of when the 'S' is read
    // The "0" is a flag for if the data has been saved to the SD card, it is present in the raw 
    // data table, but is removed from the formatted data table. 0 = not saved, 1 = saved.
    timeOfNewData = now();
    data = "0" + String(timeOfNewData) + "\t";   

    data.concat(String(character));                 // Adds the 'S' that was detetected to the data string.        

    // Reads from Serial1, byte by byte, and adds the char that was read
    // until the terminating char '@' is read. 
    // Serial.print("Entering loop to read Serial1..."); // testing
    while (character != '@') {                      // ASCII code for '@' = 64
      while(Serial1.available()) {      
        character = Serial1.read();
        data.concat(String(character));
        if (character == '@') {
          break;
        }
      }
    }
    // Serial.println("exited loop."); // testing

    // Serial.println("Beginning publishing data."); // testing
    // Returns 1 or 3 if Ethernet connection is not maintained. 
    // Returns 2 or 4 if renewal/rebind successful. 0 = nothing happened/renewal was not needed.
    byte ethReturnByte = Ethernet.maintain(); 
    Serial.println("Ethernet return byte: " + String(ethReturnByte)); // testing
    // Checks if Ethernet connection is still good(and updates IP from DHCP if needed) 
    if (ethReturnByte == 2 || ethReturnByte == 4 || ethReturnByte == 0) {
      // Since ethernet is available, syncs the time to NTP if previous sync was >= 24 hrs ago.
      if (now() >= timeOfLatestSync + 86400000) {   // 86400000 ms = 24 hrs 
        setup_NTP();
      }
      // Since ethernet is available, attempts to publish data via mqtt protocol.
      commence_connection();
      if (!mqttClient.connected()) {      // if first connection fails, try just 1 more time.
        commence_connection();
        if (!mqttClient.connected()) {    // if second attempt fails, just save to the SD card and move on.
          Serial.println("MQTT not connected");
          if (!setup_SD()) {
            Serial.println("Unable to setup SD. Data Lost Forever.");  // This means the data was not published nor saved to the SD.
          } else {
            data[0] = '1';
            unpublishedToSD(data, timeOfNewData);
          }
        }
      } else {
        if (setup_SD()) {
          data[0] = '1';
          publishedToSD(data, timeOfNewData);
          publish_string(topic, data);
          Serial.println("Publication topic: " + topic); 
        } else {
          publishedToSD(data, timeOfNewData);
          publish_string(topic, data);
          Serial.println("Publication topic: " + topic); 
        }
      }
    }
    // If ethReturnByte returns 1 or 3:
    else {
      Serial.println("Ethernet not connected, maintain() returned " + ethReturnByte);
      if (!setup_SD()) {
        Serial.println("Unable to setup SD. Data Lost Forever.");  // This means the data was not published nor saved to the SD.
      } else {
        data[0] = '1';
        unpublishedToSD(data, timeOfNewData);
      }
    }
  }

  // For testing
  Serial.print("Data: ");
  Serial.println(data);

  // This section attempts to publish data that was not published but stored in the SD/
  // It does this until it has been 30 seconds since the last data request to arduino.
  if (setup_SD()) {
    File unpublishedFolder = SD.open("unpublished/");
    while ((millis() < (millisOfRequest + 30000))) {
      File unpublishedFile = unpublishedFolder.openNextFile();                  
      if (unpublishedFile) {                                                    // Checks if folder contains any files
        byte ethReturnByte = Ethernet.maintain();                               
        if (ethReturnByte == 2 || ethReturnByte == 4 || ethReturnByte == 0) {   // Checks for good ethernet connection
          commence_connection();                                                 
          if (mqttClient.connected()) {                                         // Checks for good mqtt client connection
            processUnpublishedFile(unpublishedFile);
            unpublishedFile.close();
          }
        }
      }
      delay(500); // Will writing really quickly degrade the SD card? Not sure how long we should wait if so.
    }
    unpublishedFolder.close();
  } else {
    while ((millis() < (millisOfRequest + 30000)));
  }
}

// Clears the Serial1 buffer. 
void clearSerial1Buffer() {
  // Serial.print("Clearing serial buffer..."); // testing
  while (Serial1.available()) {
    Serial1.read();
  }
  // Serial.println("cleared."); // testing
}

// NTP Functions. Copied straight out of /Examples/Time/TimeNTP.ino
const int NTP_PACKET_SIZE = 48; // NTP time is in the first 48 bytes of message
byte packetBuffer[NTP_PACKET_SIZE]; //buffer to hold incoming & outgoing packets

time_t getNtpTime()
{
  while (Udp.parsePacket() > 0) ; // discard any previously received packets
  Serial.print("Transmit NTP Request...");
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
      Serial.print("TIME: ");
      Serial.println(secsSince1900 - 2208988800UL + timeZone * SECS_PER_HOUR);
      return secsSince1900 - 2208988800UL + timeZone * SECS_PER_HOUR;
    }
  }
  Serial.println("No NTP Response :-(");
  return getTeensy3Time(); // return time from teensy internal clock if unable to get the time with NTP
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


