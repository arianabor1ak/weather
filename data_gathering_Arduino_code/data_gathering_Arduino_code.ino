#include <TimeLib.h>

//------------------------------------------------------------------------------------------------------------------------------------------------------------
String data;
String teensy_data;
String b_data;                       // this is the bottom of the tower data, including 30V power supply, approx. 130 fields
String one_data;                     // this is the top sections multiplexer data, or misc data from various sensors, approx. 83 fields
String two_data;                     // this is the sway sensor data, approx. 80 fields
String three_data;                   // this is the flux sensor data, approx. 62 fields
String four_data;                    // this is the traixial magnetometer data, approx. 83 fields
String kz_data;                      // this is the top section aux power supply data
String stringToSend = "";                 // this is the concantenated string of the above sub-strings of data that comprises the tower data.

//-------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//                initialization
//
//-------------------------------------------------------------------------------------------------------------------------------------------------------------

void setup()
{
  Serial.begin(9600);                    // this is the baud rate for all the data from the tower: the bottom section and top section
  Serial1.begin(57600);                   // this is the baud rate that the Arduino sends the concantenated string of data to the teensy
                                          //
  Serial.print("QQ");                     // send a QQ to start the data collection
  // delay(13000);                           // wait up to 13 seconds for the data to be collected

  b_data = getData("SS", 10000);                 // read the bottom section data including 30 volt supply
    
  one_data = getData("11", 5000);               // read the top section mux data
    
  two_data = getData("22", 5000);               // read the top section sway sensor data
    
  three_data = getData("33", 5000);             // read the top section flux data

  four_data = getData("44", 5000);              // read the top section triaxial magnetometer sensor data
    
  Serial.flush();
  Serial.begin(38400);
  kz_data = getData("KZ", 5000);              // read the top section aux power supply data
  Serial.flush();
  Serial.begin(9600);

  stringToSend = "S-\t" + b_data + "1-\t" + one_data + "2-\t" + two_data + "3-\t" + three_data + "4-\t" + four_data + "Z-\t" + kz_data + "@";
}

//---------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//              MAIN LOOP
//              When the teensy sends a "GD" (Get Data) then send the previously collected data from the Arduino to the teensy.  **  HOW TO HANDLE THE "ACTIONS"
//              Once the data is sent to the teensy the Arduino sends a QQ to the tower bottom PIC to tell it to start collecting the data again.  Since the 
//              data collection process can take up to 13 seconds the Arduino waits 13 seconds doing nothing.  It then sends an "SS" to collect the bottom
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

      int stringLength = stringToSend.length();
      while(stringLength > 0) //while there are still characters in the string
      {
        int j = 0;
        while (j < 30 && stringLength > 0) //write 30 bytes at a time
        {
          Serial1.write(stringToSend.charAt(0)); //write one byte to the buffer
          stringToSend.remove(0, 1); //remove the first character from the string
          stringLength--;
          j++;
        }
        delay(75); //wait for the Teensy to read from the buffer
      }

      Serial.print("QQ");                       // send a QQ to start the data collection
      // delay(13000);                          // wait up to 13 seconds for the data to be collected
      //not sure if the delay is necessary since it's not affecting anything yet
   
      b_data = getData("SS", 10000);                 // read the bottom section data including 30 volt supply
    
      one_data = getData("11", 5000);               // read the top section mux data
    
      two_data = getData("22", 5000);               // read the top section sway sensor data
    
      three_data = getData("33", 5000);             // read the top section flux data

      four_data = getData("44", 5000);              // read the top section triaxial magnetometer sensor data
    
      Serial.flush();
      Serial.begin(38400);
      kz_data = getData("KZ", 5000);              // read the top section aux power supply data
      Serial.flush();
      Serial.begin(9600);

      //concatenate the string before the Teensy requests more data
      stringToSend = "S-\t" + b_data + "1-\t" + one_data + "2-\t" + two_data + "3-\t" + three_data + "4-\t" + four_data + "Z-\t" + kz_data + "@";
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
 * letter. In the case of this project,
 * the letters that will return data 
 * are 'P', 'T', 'B', and '1' -> that is a one
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
