#include <TimeLib.h>

//------------------------------------------------------------------------------------------------------------------------------------------------------------
// char teensy_data[3];
String teensy_data;
// char s_data[200];
// char one_data[130];
// char two_data[100];
// char three_data[100];
// char four_data[100];
// char kz_data[60];
// char stringList[6] = {s_data, one_data, two_data, three_data, four_data, kz_data};                // this is the concantenated string of the above sub-strings of data that comprises the tower data.
String stringList[6];

//-------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//                initialization
//
//-------------------------------------------------------------------------------------------------------------------------------------------------------------

void setup()
{
  delay(125000);
  
  Serial.begin(57600);                    // this is the baud rate for all the data from the tower: the bottom section and top section
  Serial1.begin(57600);                   // this is the baud rate that the Arduino sends the concantenated string of data to the teensy

  Serial.print("QQ");                     // send a QQ to start the data collection
  delay(15000);                           // wait 20 seconds for the data to be collected

  stringList[0] = "S-\t" + getData("SS", 3000);                 // read the bottom section data including 30 volt supply
    
  stringList[1] = "\t1-\t" + getData("11", 3000);               // read the top section mux data
    
  stringList[2] = "\t2-\t" + getData("22", 3000);               // read the top section sway sensor data
    
  stringList[3] = "\t3-\t" + getData("33", 3000);             // read the top section flux data

  stringList[4] = "\t4-\t" + getData("44", 3000);              // read the top section triaxial magnetometer sensor data
    
  Serial.flush();
  Serial.begin(38400);

  stringList[5] = "\tZ-\t" + getData("KZ", 3000);              // read the top section aux power supply data
  Serial.flush();
  Serial.begin(57600);
}

//---------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//              MAIN LOOP
//              When the teensy sends a "GD" (Get Data) then send the previously collected data from the Arduino to the teensy.  **  HOW TO HANDLE THE "ACTIONS"
//              Once the data is sent to the teensy the Arduino sends a QQ to the tower bottom PIC to tell it to start collecting the data again.  Since the 
//              data collection process can take up to 13 seconds the Arduino waits longer for collecting B data.  It then sends an "SS" to collect the bottom
//              section data.  After that data is received it sends 11, 22, 33, 44, 55 to gather data from the top section sensors.  Gathering data should be
//              should be pretty quick so the whole "update bottom data, wait, read the bottom data, read the top data" should be about 15 seconds.
//
//
//---------------------------------------------------------------------------------------------------------------------------------------------------------------

void loop()
{
    teensy_data = "";
    if (Serial1.available())                 // this is data that already arrived and is available in the serial buffer
  {
      teensy_data = Serial1.readString();     // if there is data available read it into "data".  Looking for a "GD" from the teensy to send the data to the 
      clearSerial1Buffer();                     // teensy and then update the Arduino strings.
  }
    
    if (teensy_data == "GD")                       // the teensy tells the arduino to Gather the Data.  The teensy then waits for the Arduino to send the data   
    {                                         // the teensy reads the string of data.  Once it has it the Arduino collects the updated data.
      
      int data;
      for (data = 0; data < 6; data++) {
        Serial1.print(stringList[data]);
        delay(300);
      }
      Serial1.print("\t@");

      Serial.print("QQ");                       // send a QQ to start the data collection
      delay(15000);
   
      stringList[0] = "S-\t" + getData("SS", 3000);                 // read the bottom section data including 30 volt supply
    
      stringList[1] = "\t1-\t" + getData("11", 3000);               // read the top section mux data
        
      stringList[2] = "\t2-\t" + getData("22", 3000);               // read the top section sway sensor data
        
      stringList[3] = "\t3-\t" + getData("33", 3000);             // read the top section flux data

      stringList[4] = "\t4-\t" + getData("44", 3000);              // read the top section triaxial magnetometer sensor data
        
      Serial.flush();
      Serial.begin(38400);

      stringList[5] = "\tZ-\t" + getData("KZ", 3000);              // read the top section aux power supply data
      Serial.flush();
      Serial.begin(57600);
    }
}

/*
 * ------------------------------------------------------------------------------------
 *  The following functions relate to getting the Multiplexer data.
 * ------------------------------------------------------------------------------------
 */
 
/*
 * Input a letter, and the output will
 * be the data that corresponds to that 
 * letter.
 */
String getData(String letters, unsigned long delayMillis){
  Serial.print(letters);
  unsigned long timeOfCall = millis();

  String data = "";
  char byte = 'a';

  while (byte != '\r' && (millis() < (timeOfCall) + delayMillis)) {  //read all the data until a carriage return
    while (Serial.available()) {
      byte = Serial.read();
      if (byte == '\r')   //don't add byte to the data if it is a carriage return
      {
        break;
      }
      data += byte;
    }
  }
  clearSerialBuffer();
  delay(300);
  return data;
}

/*
 * Ensures that nothing is 
 * in the input buffer once
 * we try requesting a new 
 * letter.
 */
void clearSerialBuffer()
{
  while (Serial.available()) 
  {
    Serial.read();
  }
}

void clearSerial1Buffer()
{
  while (Serial1.available()) 
  {
    Serial1.read();
  }
}
