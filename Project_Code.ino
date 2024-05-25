/*
* Project_Code
* Code for the arduino part of the project
* Reads a voltage from one of two possible pins and sends it to the raspberry Pi
*/

//Include for the I2C communication and another so that voltages can be converted to strings and trasnmitted
#include <Wire.h>
#include <floatToString.h>

//Constant used to convert arduino reading to an actual voltage. The base readings are from 0-1024, being proportional to how much the voltage is to the reference voltage.
//For the Arduino Nano, the reference is 3.3V, thus dividing by 1024 and multiplying by 3.3 converts to an actual voltage 
const double RATIO = (3.3 / 1024.0);

//Global variable for the currently held voltage of the arduino
char value[5] = "NULL";

void setup() 
{
  //Sets up serial and slave part of I2C
  Serial.begin(9600);
  Wire.begin(9);

  //Sets up onRecieve() and onRequest(), which is what this arduino will do when getting prompted by the raspberry pi
  Wire.onReceive(calculateInfo);
  Wire.onRequest(sendInfo);
}

void loop() 
{
  //Was only used for debugging. The functionality is entirely from the other methods in the project file
  /*
  if (Serial.read() == 'A')
  {
    getAA();
  }

  else if (Serial.read() == 'B')
  {
    getAAA();
  }

  delay(100);
  */
}

//Method to get the voltage of the AA battery from pin 0
void getAA()
{
  //Initialises variables to represent the current and total measured voltages
  float reading = 0;
  float total = 0;

  //To get a better idea of the actual voltage, takes an average value over 1 second for each size of battery
  //For loop for the AA battery
  Serial.println("Measuring AA...");
  for (int i = 0; i < 10; i ++)
  {
    //Gets current voltage and adds it to total. Uses two variables, one for the current voltage and one for the total
    reading = analogRead(0);
    total += reading;
    delay(100);
  }

  //Divides total by 10 to get an average and multiplies by RATIO to get an actual voltage
  total /= 10;
  total *= RATIO;

  //Converts to char array
  floatToString(total, value, 5, 2);

  Serial.print("Voltage AA: ");
  Serial.print(value);
  Serial.println(" V");
  Serial.println();
}

//Method to get the voltage of the AAA battery from 1 
void getAAA()
{
  //Initialises variables to represent the current and total measured voltages
  float reading = 0;
  float total = 0;

  Serial.println("Measuring AAA...");
  for (int i = 0; i < 10; i ++)
  {
    //Gets current voltage and adds it to total
    reading = analogRead(1);
    total += reading;
    delay(100);
  }

  //Divides total by 10 to get an average and multiplies by RATIO to convert it to a voltage
  total /= 10;
  total *= RATIO;

  //Converts to a string
  floatToString(total, value, 5, 2);

  Serial.print("Voltage AAA: ");
  Serial.print(value);
  Serial.println(" V");
  Serial.println();
}

//Method that actives when I2C is recieved. Depending on the recieved byte, picks either getAA or getAAA
void calculateInfo(int byteNumber)
{
  //Default variable for byte, a variable to represent the integer sent by the raspberry pi
  int byte = 26;

  //Loops through each bit sent by the pi, saving the last one. The pi sends two bits, a control and the actual data, of which the last is what is used
  while (Wire.available())
  {
    byte = Wire.read();
  }

  //Checks if the byte sent was a 1, meaning a AA request
  if (byte == 1)
  {
    getAA();
  }

  //If a 2, measures AAA instead
  else if(byte == 2)
  {
    getAAA();
  }
}

//Method that activates when I2C is requested by pi. Simply sends whatever value has been calulated to to pi.
void sendInfo()
{
  if (Wire.available())
  {
    Wire.write(value);
  }
}
