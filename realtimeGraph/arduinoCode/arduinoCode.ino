#include "SparkFunHTU21D.h"

#include <DynamixelSerial3.h>

HTU21D myHumidity;
const int PWML=6;
const int PWMR=5;
const int DIRL=7;
const int DIRR=4;
int pinTrig = 11;
int pinEcho = 12;
long temps ;
float vitdynam=80;
float R;
float a=17.5;
float b=40;
float sens;
float temperature = 30;
float humidity = 70;
float distance = 0 ; 
String message = "", commande;
float alpha ;
int vitesse = 0; 
char readbuffer[16] ;
void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT);
  pinMode(12, INPUT);
  digitalWrite(11, LOW);
  Serial1.begin(57600);
  //Serial1.begin(115200);
  myHumidity.begin();
  delay(200);
  Dynamixel.begin(1000000, 2); // Inicialize the servo at 1Mbps and Pin Control 2
  Dynamixel.setEndless(1, OFF);
  Dynamixel.setEndless(2, OFF);
  Dynamixel.moveSpeed(1, 512, vitdynam);
  Dynamixel.moveSpeed(2, 512, vitdynam);
  pinMode(PWMR, OUTPUT);
  pinMode(PWML, OUTPUT);
  pinMode(DIRR, OUTPUT);
  pinMode(DIRL, OUTPUT);
  Serial1.println("com");
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial1.available() > 0  ) {  
      // fonction pour traiter les données reçues à partir du moniteur ( surtout le format)     
      readFromSensors();
      handleComingData();
  } 
  delay(50);   
  
}
void handleComingData(){
 int readCharacter = Serial1.readBytesUntil('\n', readbuffer, 20); 
      message = ""; 
      for(int i = 0 ; i< readCharacter; i++){
        message += readbuffer[i];
      }
      if (message == "SENSOR"){
        Serial1.print(temperature);
        Serial1.print(" ");
        Serial1.print(humidity);
        Serial1.print(" ");
        Serial1.println(distance);
      }
      else {
        commande = message.substring(0,message.indexOf(' '));
        alpha = message.substring(message.indexOf(' '),message.lastIndexOf(' ')).toFloat(); 
        vitesse = message.substring(message.lastIndexOf(' ')).toFloat();
        if (commande == "ACTION"){
          takeAction();
        }
      }
}  
void readFromSensors(){
  temperature = myHumidity.readTemperature();
  humidity = myHumidity.readHumidity();
  digitalWrite(11, HIGH);
  delayMicroseconds(50);
  digitalWrite(11, LOW);
  temps = pulseIn(12, HIGH);
    if (temps <= 24000) 
  {
    distance = temps*0.034/2;
  }
}
void takeAction(){
  
  rayon(alpha);
  if(R>a){
       movemotors(vitesse, -vitesse);
      }
   else {
       movemotors(vitesse, vitesse);
      }
  Serial1.println("ok");      
}

void movemotors(float VR,float VL){
  if (VR>=0){
    analogWrite(PWMR,abs(VR));
    digitalWrite(DIRR,HIGH);
    }
  else {
    analogWrite(PWMR,abs(VR));
    digitalWrite(DIRR,LOW);
    }
  if (VL>=0){
    analogWrite(PWML,abs(VL));
    digitalWrite(DIRL,HIGH);
    }
  else {
    analogWrite(PWML,abs(VL));
    digitalWrite(DIRL,LOW);
    }
  }
void rayon(float angle) {
  if (angle==0){
    R=10000;
    }
  else{
    R=b/tan(angle*PI/180);
    }
  float alpha1 = atan(b / (R - a));
  float alpha2 = atan(b / (R + a));
  alpha1 = (alpha1 * (180.0 / PI)) * (1023.00 / 300);
  alpha2 = (alpha2 * (180.0 / PI)) * (1023.00 / 300);
  Dynamixel.moveSpeed(3, 512 + alpha1, vitdynam);
  Dynamixel.moveSpeed(4, 512 + alpha2, vitdynam);
  Dynamixel.moveSpeed(2, 512 - alpha1, vitdynam);
  Dynamixel.moveSpeed(1, 512 - alpha2, vitdynam);
  }
