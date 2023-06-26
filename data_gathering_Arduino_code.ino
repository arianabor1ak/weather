


//------------------------------------------------------------------------------------------------------------------------------------------------------------
String data;
String b_data = "";                       // this is the bottom of the tower data, including 30V power supply, approx. 170 fields
String one_data = "";                     // this is the top sections multiplexer data, or misc data from various sensors, approx. 115 fields
String two_data = "";                     // this is the sway sensor data, approx. 80 fields
String three_data = "";                   // this is the flux sensor data, approx. 62 fields
String four_data = "";                    // this is the traixial magnetometer data, approx. 83 fields
String five_data = "";                    // this is a placemarker for future data from the top. Or from the bottom or something new. 
String stringToSend = "";                 // this is the concantenated string of the above sub-strings of data the comprises the tower data.

//-------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//                initialization
//
//-------------------------------------------------------------------------------------------------------------------------------------------------------------

void setup() 
{
  Serial.begin(57600);                    // this is the baud rate for all the data from the tower: the bottom section and top section
  Serial1.begin(57600);                   // this is the baud rate that the Arduino sends the concantenated string of data to the teensy
                                          //
  Serial.print("QQ");                     // send a QQ to start the data collection
  delay(13000);                           // wait up to 13 seconds for the data to be collected
}

//---------------------------------------------------------------------------------------------------------------------------------------------------------------
//
//              MAIN LOOP
//              When the teensy sends a "GD" (Get Data) then send the previously collected data from the Arduino to the teensy.  **  HOW TO HANDLE THE "ACTIONS"
//              Once the data is sent to the teensy the Arduino sends a QQ to the tower bottom PIC to tell it to start collecting the data again.  Since the 
//              data collection process can take up to 13 seconds the Arduino waits 13 seconds doing nothing.  It then sends an "SS" to collect the bottom
//              section data.  After tht datais received it sends 11, 22, 33, 44, 55 to gather data from the top section sensors.  Gathering data should be
//              should be pretty quick so the whole "update bottom data, wait, read the bottom data, read the top data" should be about 15 seconds.
//
//
//---------------------------------------------------------------------------------------------------------------------------------------------------------------

void loop()
{
    if (Serial1.available());                 // this is data that already arrived and is available in the serial buffer
  {
      String data = Serial1.readString();     // if there is data available read it into "data".  Looking for a "GD" from the teensy to send the data to the 
      clearInputBuffer();                     // teeensy and then update the Arduino strings.
  }
    
    if (data == "GD");                        // the teensy tells the arduino to Gather the Data.  The teensy then waits for the Arduino to send the data   
    {                                         // the teensy reads the string of data.  Once it has it the Arduino collects the updated data.
      
      String stringToSend = "S-" + b_data + "1-" + one_data + "2-" + two_data + "3-" + three_data + "4-" + four_data + "5-" + five_data + "@";         
      Serial1.print(stringToSend);
      //waitMicroseconds(5000);      

    Serial.print("QQ");                       // send a QQ to start the data collection
    delay(13000);                             // wait up to 13 seconds for the data to be collected
   
      b_data = getData("SS");                 // read the bottom section data including 30 volt supply
      //waitMicroseconds(5000);       
      //clearInputBuffer();
    
      one_data = getData("11");               // read the top section mux data
      //waitMicroseconds(5000);
      //clearInputBuffer();
    
      two_data = getData("22");               // read the top section sway sensor data
      //waitMicroseconds(5000);                                                                                         
      //clearInputBuffer();
    
      three_data = getData("33");             // read the top section flux data
      //waitMicroseconds(5000);
      //clearInputBuffer(); 

      four_data = getData("44");              // read the top section triaxial magnetometer sensor data
      //waitMicroseconds(5000);
      //clearInputBuffer();
    
      five_data = getData("55");              // read the top section future data, acts as a placeholder for future data
      //waitMicroseconds(5000);
      //clearInputBuffer(); 
    }

}


/*
 * This is used as an alternative to 
 * the delay() function. The millis() 
 * approach is recommended over the
 * delay() approach. In the case of 
 * this project, delay() also doesn't
 * seem to work.
 */
void waitMicroseconds(long wait_time) 
{
  unsigned long current_time = millis();
  while (millis() < current_time + wait_time)
  {
    
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
String getData(String letters){
  unsigned long current_time = millis();
  String data = "";
  Serial.print(letters);
  while (millis() < current_time + 5000) 
  {
    if (Serial.available()) 
    {
      data = Serial.readString();
      break;
    }
  }
  //Serial.println(data);
  return data;
}

/*
 * Ensures that nothing is 
 * in the input buffer once
 * we try requesting a new 
 * letter.
 */
void clearInputBuffer() 
{
  while (Serial.available()) 
  {
    Serial.read();
  }
}
