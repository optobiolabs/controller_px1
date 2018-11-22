// include the library codes for LCD, temperature sensor 
#include <LiquidCrystal.h>
#include <OneWire.h>
#include <DallasTemperature.h>
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 8,7, 5, 4, 2);

// define PINs
#define LCD_LIGHT_PIN A4  //toggle LCD backlight
#define ONE_WIRE_BUS 14   //temperature

// define external power sensor
const int extPowerPin = 13;
int extPowerState = HIGH;

// analog PIN LDR
int PIN_LDR = 1;

const int statusLED1 = 16;
const int statusLED2 = 17;

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);
 
// Pass oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

// read data from serial
char rc;

unsigned long time;

// array to store the received data
const byte numChars = 250;
//char receivedChars[numChars];

//1,2,3;4,5,6:7,8,9

// execute function only with new data
boolean newData = false;

//char loops[6];

// 4 PWM channels for LEDs
const int ledPin1 = 9;
const int ledPin2 = 10;

const int ledPin3 = 3;
const int ledPin4 = 11;

const int numInt = 40;

int intensity1;
int intensity2;

//int intensities3[numInt];
//int intensities4[numInt];

unsigned long duration1;
unsigned long duration2;

unsigned long start1;
unsigned long start2;
//int steps;

char* ch1;
char* ch2;

void setup() {
  // D9 & D11
  TCCR1B = TCCR1B & B11111000 | B00000001;    // set timer 1 divisor to     1 for PWM frequency of 31372.55 Hz
  // D3 & D11
  TCCR2B = TCCR2B & B11111000 | B00000001;    // set timer 2 divisor to     1 for PWM frequency of 31372.55 Hz

  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.print("  opto biolabs");
  lcd.setCursor(0,1);
  lcd.print("     PX ONE");
  // temperature sensor
  sensors.begin();

  delay(1000);
  Serial.begin(115200);
  Serial.println("<controller ready>");

  // LCD detector
  pinMode(LCD_LIGHT_PIN, OUTPUT);
  digitalWrite(LCD_LIGHT_PIN, HIGH);
  pinMode(extPowerPin, INPUT);

  pinMode(statusLED1, OUTPUT);
  pinMode(statusLED2, OUTPUT);
    
  LEDoff();
}

void LEDoff() {
  analogWrite(ledPin1, 0);
  analogWrite(ledPin2, 0);
  analogWrite(ledPin3, 0);
  analogWrite(ledPin4, 0);
}

void LCDpower() {
  extPowerState = digitalRead(extPowerPin);

  if (extPowerState == HIGH)
  {
    digitalWrite(LCD_LIGHT_PIN, HIGH);
    }
    else
    {
      digitalWrite(LCD_LIGHT_PIN, LOW);
    }
}

void read_channels() {
    if (Serial.available() > 0) {
      String ch1 = Serial.readStringUntil(':');
      Serial.read();
      String ch2 = Serial.readStringUntil('\n');
      Serial.read();

      char delim[1] = ";"; 
      
      int intensity1;
      int intensity2;
      
      unsigned long start1 = 0L;
      unsigned long start2 = 0L;

      unsigned long duration1 = 0L;
      unsigned long duration2 = 1L;

      char str_array1[ch1.length()+1];
      ch1.toCharArray(str_array1, ch1.length()+1);
      
      char str_array2[ch2.length()];
      ch2.toCharArray(str_array2, ch2.length());
      
      lcd.clear();

      for (char *token1 = strtok(str_array1,delim); token1 != NULL; token1 = strtok(NULL, delim)){
        sscanf(token1,"%lu,%d,%lu", &start1, &intensity1, &duration1);
        Serial.println(intensity1);

        lcd.setCursor(0,0);
        lcd.print(intensity1);
        analogWrite(ledPin1, 35 + intensity1*2.2);
        analogWrite(ledPin2, 35 + intensity1*2.2);
      }
      
      for (char *token2 = strtok(str_array2,delim); token2 != NULL; token2 = strtok(NULL, delim)){
        sscanf(token2,"%lu,%d,%lu",&start2, &intensity2, &duration2);
        Serial.println(intensity2);
        
        lcd.setCursor(0,1);
        lcd.print(intensity2);
        analogWrite(ledPin3, 35 + intensity2*2.2);
        analogWrite(ledPin4, 35 + intensity2*2.2);
      }
      
      
       
      
    }
}

void read_temperature() {
  // Call sensors.requestTemperatures() to issue a global temperature and Requests to all devices on the bus
  sensors.requestTemperatures(); 
  
  
  // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  double temperature = sensors.getTempCByIndex(0);
  Serial.print(temperature); 
  Serial.println("°C");

  if (temperature < 24) {
    digitalWrite(statusLED1, HIGH); 
    Serial.println("off");
  }
  else {
    digitalWrite(statusLED1, LOW);
    Serial.println("on");
  }
}

double Light (int RawADC0)
{
  double Vout=RawADC0*0.0048828125;
  int lux=500/(10*((5-Vout)/Vout));//use this equation if the LDR is in the upper part of the divider
  //int lux=(2500/Vout-500)/10;
  return lux;
}

void read_light(){
  
  int light = int(Light(analogRead(PIN_LDR)));
  Serial.print(light);
  Serial.println(" Lux");

  if (light < 60) {
    digitalWrite(statusLED2, HIGH); 
    Serial.println("off");
  }
  else {
    digitalWrite(statusLED2, LOW);
    Serial.println("on");
  }

}

void loop() {
  LCDpower();
  read_channels();
  read_temperature();
  read_light();
  
}


