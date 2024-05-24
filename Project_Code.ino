/*
* Project_Code
* Code for the arduino part of the project
* Reads a voltage from one of two possible pins and sends it to the raspberry Pi
*/

//Include for the I2C communication
#include <Wire.h>

//Constant used to convert arduino reading to an actual voltage. The base readings are from 0-1024, being proportional to how much the voltage is to the reference voltage.
//For the Arduino Nano, the reference is 3.3V, thus dividing by 1024 and multiplying by 3.3 converts to an actual voltage 
const double RATIO = (3.3 / 1024.0);

void setup() 
{
  //Sets up serial and slave part of I2C
  Serial.begin(9600);
  Wire.begin(26);

  //Sets up onRequest(), which is what this arduino will do when getting a request
  Wire.onRequest(sendInfo);
}

void loop() 
{
  //Was only used for debugging. The functionality is entirely from the other methods in the project file
  if (Serial.read() == 'A')
  {
    getAA();
  }

  else if (Serial.read() == 'B')
  {
    getAAA();
  }

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

  //Divides total by 10 to get an average
  total /= 10;

  Serial.print("Voltage AA: ");
  Serial.print(total * RATIO);
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

  //Divides total by 10 to get an average
  total /= 10;

  Serial.print("Voltage AAA: ");
  Serial.print(total * RATIO);
  Serial.println(" V");
  Serial.println();
}

//Method that actives when I2C is recieved. Depending on the recieved byte, picks either getAA or getAAA
void sendInfo()
{
  //Checks if the byte sent was a 1, meaning a AA request
  if (Wire.read() == '1')
  {
    getAA();
  }

  //If a 2, measures AAA instead
  else if(Wire.read() == '2')
  {
    getAAA();
  }
}
