// *   Pad 1, Pad 5: Vin (Voltage input 4.5V-6V)
// *   Pad 2, Pad 3, Pad 12: GND
// *   Pad 6: PWM output ==> pin 8
#define DHTTYPE DHT11


#include "DHT.h"   // Librairie des capteurs DHT
#define DHTPIN 2    // pin sur lequel est branché le DHT
DHT dht(DHTPIN, DHTTYPE); 
byte Octet = 0;
char  RX = 0;         // Variable pour la mesure
byte  MonEntreeNumerique = 2;
const int pwmPin1 = 9;     // broche PWM 9
const int pwmPin2 = 10;
const int pwmPin3 = 11;

void setup() 
{
  Serial.begin(9600);           //Config du port série
  pinMode(pwmPin1, INPUT_PULLUP);     // initialisation des capteurs en input
  pinMode(pwmPin2, INPUT_PULLUP);
  pinMode(pwmPin3, INPUT_PULLUP);
  dht.begin();
  while (Serial == false)       // L'objet Serial renvoie true quand la connection est prête.
  {                             // Tant que la réponse est false, on ne fait rien ...
    delay(1);
  }
}

void loop()
{
   if (Serial.available() > 0) // Test de reception
  {
    RX = Serial.read();

    // Mesure de temps depuis le démarrage en millisecondes:
    if (RX == 'T') // recupere mesure si T
    {
      
        // Serial.print('m');
      float concentration1 = concentration_PWM1();
      float concentration2 = concentration_PWM2();
      float concentration3 = concentration_PWM3();
      float humidite = dht.readHumidity();
      float temperature = dht.readTemperature();
  //long temps = millis(); 

      Serial.print(millis()/1000);
     //Serial.print(temps);
     Serial.print(';');
     Serial.print(concentration1);
     Serial.print(';');
     Serial.print(concentration2);
     Serial.print(';');
     Serial.print(concentration3);
     Serial.print(';');
     Serial.print(temperature);
     Serial.print(';');
     Serial.println(humidite);
     
     // Stop le programme et renvoie un message d'erreur si le capteur ne renvoie aucune mesure
     if (isnan(humidite) || isnan(temperature)) {
        Serial.println("Echec de lecture !");
        return;
      }   
    }
  }  
}


int concentration_PWM1()   //Fonction pour avoir la concentration des capteurs 
{
  while (digitalRead(pwmPin1) == LOW) {};
  long t0 = millis();
  while (digitalRead(pwmPin1) == HIGH) {};
  long t1 = millis();
  while (digitalRead(pwmPin1) == LOW) {};
  long t2 = millis();
  long tH = t1-t0;
  long tL = t2-t1;
  long ppm = 5000 * (tH - 2) / (tH + tL - 4);
  while (digitalRead(pwmPin1) == HIGH) {};
  
  return int(ppm);
}

int concentration_PWM2()   //Fonction pour le PWM
{
  while (digitalRead(pwmPin2) == LOW) {};
  long t0 = millis();
  while (digitalRead(pwmPin2) == HIGH) {};
  long t1 = millis();
  while (digitalRead(pwmPin2) == LOW) {};
  long t2 = millis();
  long tH = t1-t0;
  long tL = t2-t1;
  long ppm = 5000 * (tH - 2) / (tH + tL - 4);
  while (digitalRead(pwmPin2) == HIGH) {};
  
  
  return int(ppm);
  }
int concentration_PWM3()   //Fonction pour le PWM
{
  while (digitalRead(pwmPin3) == LOW) {};
  long t0 = millis();
  while (digitalRead(pwmPin3) == HIGH) {};
  long t1 = millis();
  while (digitalRead(pwmPin3) == LOW) {};
  long t2 = millis();
  long tH = t1-t0;
  long tL = t2-t1;
  long ppm = 5000 * (tH - 2) / (tH + tL - 4);
  while (digitalRead(pwmPin3) == HIGH) {};
  
  
  return int(ppm);
  }
  
