
#include "IRremote.h"

const int pinIR = 2;   // Broche de réception IR
const int pinLED = 3;  // Broche de contrôle des LEDs

IRrecv irrecv(pinIR);
decode_results irResults; // create a results object of the decode_results class

// Configuration des codes IR pour chaque bouton de la télécommande
const unsigned long codeBouton1 = 0xFFA25D;
const unsigned long codeBouton2 = 0xFF629D;
const unsigned long codeBouton3 = 0xFFE21D;

void translateIR()

{

  switch(irResults.value)

  {
  case 0xFFA25D: Serial.println("B+"); break;
  case 0xFFE21D: Serial.println("O"); break;
  case 0xFF629D: Serial.println("B-"); break;
  case 0xFF22DD: Serial.println("FAST BACK");    break;
  case 0xFF02FD: Serial.println("PAUSE");    break;
  case 0xFFC23D: Serial.println("-");   break;
  case 0xFFE01F: Serial.println("change blop");    break;
  case 0xFFA857: Serial.println("change dégradé");    break;
  case 0xFF906F: Serial.println("UP");    break;
  case 0xFF9867: Serial.println("EQ");    break;
  case 0xFFB04F: Serial.println("ST/REPT");    break;
  case 0xFF6897: Serial.println("0");    break;
  case 0xFF30CF: Serial.println("rouge");    break;
  case 0xFF18E7: Serial.println("vert");    break;
  case 0xFF7A85: Serial.println("marine");    break;
  case 0xFF10EF: Serial.println("orange");    break;
  case 0xFF38C7: Serial.println("vert eau");    break;
  case 0xFF5AA5: Serial.println("bleu");    break;
  case 0xFF42BD: Serial.println("jaune");    break;
  case 0xFF4AB5: Serial.println("violet");    break;
  case 0xFF52AD: Serial.println("rose");    break;
  case 0xFFFFFFFF: Serial.println(" REPEAT");break;  

  default: 
    Serial.println(" other button   ");

  }

  delay(500);
}

// Fonctions pour changer la couleur des LEDs
void setColorRed() {
  analogWrite(pinLED, 255, 0, 0);
}

void setColorGreen() {
  analogWrite(pinLED, 0, 255, 0);
}

void setColorBlue() {
  analogWrite(pinLED, 0, 0, 255);
}


void setup() {
  Serial.begin(9600);
  Serial.println("IR Receiver Button Decode"); 
  irrecv.enableIRIn(); // Start the receiver
  irrecv.blink13(true);

}
void loop() {
  if (irrecv.decode(&irResults)) 
  {
    translateIR(); 
    
    if (irResults.value == codeBouton1) {
      setColorRed();
    } else if (irResults.value == codeBouton2) {
      setColorGreen();
    } else if (irResults.value == codeBouton3) {
      setColorBlue();
    }
    // Ajoutez ici des conditions pour les autres boutons de votre télécommande

    irReceiver.resume(); // Attente du prochain signal IR
  }  
}
