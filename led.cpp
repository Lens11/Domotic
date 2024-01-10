#include <Arduino.h>
#include <FastLED.h>
#include <IRremote.h>

#define IR_PIN 2      // Broche de réception IR
#define LED_PIN 3     // Définir la broche de la LED
#define LED_COUNT 300 // Nombre de LEDs dans la bande

// Luminosité des leds par défaut
int BRIGHTNESS = 128; // Valeur entre 0 et 255 (0 étant éteint, 255 étant le plus lumineux)

// Fonction pour changer la luminosité des LEDs
void setBrightness(int brightness)
{
  FastLED.setBrightness(brightness);
  FastLED.show();
}

CRGBPalette16 blueVioletPalette = CRGBPalette16(
    CRGB(3, 0, 46), CRGB(16, 0, 62), CRGB(37, 0, 79), CRGB(61, 0, 100),
    CRGB(86, 0, 119), CRGB(110, 0, 136), CRGB(133, 0, 150), CRGB(156, 0, 162),
    CRGB(180, 0, 172), CRGB(204, 0, 180), CRGB(229, 0, 186), CRGB(255, 0, 191),
    CRGB(232, 0, 201), CRGB(207, 0, 209), CRGB(179, 0, 216), CRGB(147, 0, 221));
CRGBPalette16 sunrisePalette = CRGBPalette16(
    CRGB(255, 0, 0), CRGB(255, 10, 0), CRGB(255, 20, 0), CRGB(255, 30, 0),
    CRGB(255, 40, 0), CRGB(255, 50, 0), CRGB(255, 60, 0), CRGB(255, 70, 0),
    CRGB(255, 80, 0), CRGB(255, 90, 0), CRGB(255, 100, 0), CRGB(255, 110, 0),
    CRGB(255, 120, 0), CRGB(255, 130, 0), CRGB(255, 140, 0), CRGB(255, 150, 0));

CRGBPalette16 greenPalette = CRGBPalette16(
    CRGB(0, 30, 0), CRGB(0, 50, 0), CRGB(0, 80, 0), CRGB(0, 110, 0),
    CRGB(0, 150, 0), CRGB(0, 180, 0), CRGB(0, 210, 0), CRGB(0, 240, 0),
    CRGB(0, 255, 0), CRGB(50, 255, 50), CRGB(100, 255, 100), CRGB(150, 255, 150),
    CRGB(200, 255, 200), CRGB(220, 255, 220), CRGB(240, 255, 240), CRGB(255, 255, 255));

CRGB leds[LED_COUNT];

IRrecv irrecv(IR_PIN);
decode_results irResults; // create a results object of the decode_results class

// Configuration des codes IR pour chaque bouton de la télécommande
const unsigned long BrightnessP = 0xFFA25D;
const unsigned long BrightnessM = 0xFF629D;
const unsigned long SwitchOn = 0xFFE21D;
const unsigned long Chaud = 0xFF22DD;
const unsigned long SwitchOff = 0xFFC23D;
const unsigned long Flash = 0xFF02FD;
const unsigned long ChangeBlop = 0xFFE01F;
const unsigned long ChangeDeg = 0xFFA857;
const unsigned long Timer = 0xFF906F;
const unsigned long TonsVerts = 0xFF9867;
const unsigned long TonsBleus = 0xFFB04F;
const unsigned long TonsRouges = 0xFF6897;
const unsigned long Rouge = 0xFF30CF;
const unsigned long Vert = 0xFF18E7;
const unsigned long Bleu = 0xFF7A85;
const unsigned long Orange = 0xFF10EF;
const unsigned long VertEau = 0xFF38C7;
const unsigned long Ciel = 0xFF5AA5;
const unsigned long Jaune = 0xFF42BD;
const unsigned long Violet = 0xFF4AB5;
const unsigned long Rose = 0xFF52AD;

void translateIR()

{

  switch (irResults.value)

  {
  case 0xFFA25D:
    Serial.println("B+");
    break;
  case 0xFFE21D:
    Serial.println("On");
    break;
  case 0xFF629D:
    Serial.println("B-");
    break;
  case 0xFF22DD:
    Serial.println("Couleur chaude");
    break;
  case 0xFF02FD:
    Serial.println("Flash");
    break;
  case 0xFFC23D:
    Serial.println("Off");
    break;
  case 0xFFE01F:
    Serial.println("change blop");
    break;
  case 0xFFA857:
    Serial.println("change dégradé");
    break;
  case 0xFF906F:
    Serial.println("Timer");
    break;
  case 0xFF9867:
    Serial.println("Tons vert");
    break;
  case 0xFFB04F:
    Serial.println("Tons bleu");
    break;
  case 0xFF6897:
    Serial.println("Tons rouge");
    break;
  case 0xFF30CF:
    Serial.println("rouge");
    break;
  case 0xFF18E7:
    Serial.println("vert");
    break;
  case 0xFF7A85:
    Serial.println("bleu");
    break;
  case 0xFF10EF:
    Serial.println("orange");
    break;
  case 0xFF38C7:
    Serial.println("vert eau");
    break;
  case 0xFF5AA5:
    Serial.println("bleu ciel");
    break;
  case 0xFF42BD:
    Serial.println("jaune");
    break;
  case 0xFF4AB5:
    Serial.println("violet");
    break;
  case 0xFF52AD:
    Serial.println("rose");
    break;
  case 0xFFFFFFFF:
    Serial.println(" REPEAT");
    break;

  default:
    Serial.println(" other button   ");
  }

  delay(500);
}

void PaletteBlue()
{
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; // Incrémente l'index de départ pour changer la couleur

  // Défini une nouvelle couleur pour chaque LED dans la bande en utilisant la palette
  for (int i = 0; i < LED_COUNT; i++)
  {
    uint8_t colorIndex = startIndex + (i * 2);
    leds[i] = ColorFromPalette(blueVioletPalette, colorIndex, BRIGHTNESS, LINEARBLEND);
  }

  // Affiche les nouvelles couleurs sur la bande
  FastLED.show();
}

void Paletterouge()
{
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1; // Incrémente l'index de départ pour changer la couleur
  // Défini une nouvelle couleur pour chaque LED dans la bande en utilisant la palette
  for (int i = 0; i < LED_COUNT; i++)
  {
    uint8_t colorIndex = startIndex + (i * 2);
    leds[i] = ColorFromPalette(sunrisePalette, colorIndex, BRIGHTNESS, LINEARBLEND);
  }
  FastLED.show();
  delay(20);
}

void PaletteGreen()
{
  static uint8_t startIndex = 0;
  startIndex = startIndex + 1;
  for (int i = 0; i < LED_COUNT; i++)
  {
    uint8_t colorIndex = startIndex + (i * 2);
    leds[i] = ColorFromPalette(greenPalette, colorIndex, BRIGHTNESS, LINEARBLEND);
  }
  FastLED.show();
  delay(20);
}

// Fonction pour changer progressivement la couleur des LEDs
void changeColor()
{
  int a = 1;
  // Boucle de changement de couleur jusqu'à ce qu'une nouvelle commande soit reçue
  while (a = 1)
  {
    // if (irrecv.decode(&irResults))
    // { translateIR();
    // if (irResults.value != ChangeDeg ){
    // break; }}
    //  Parcours de toutes les valeurs de couleur

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(i, 0, 0);
      } // Rouge
      FastLED.show();
      delay(5);
    }

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(255, i, 0);
      } // Rouge à Jaune
      FastLED.show();
    }

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(255 - i, 255, 0);
      } // Jaune à Vert
      FastLED.show();
      delay(5);
    }

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(0, 255, i);
      } // Vert à Cyan
      FastLED.show();
      delay(5);
    }

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(0, 255 - i, 255);
      } // Cyan à Bleu
      FastLED.show();
      delay(5);
    }

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(i, 0, 255);
      } // Bleu à Magenta
      FastLED.show();
      delay(5);
    }

    for (int i = 0; i <= 255; i++)
    {
      for (int k = 0; k <= LED_COUNT; k++)
      {
        leds[k] = CRGB(255, 0, 255 - i);
      } // Magenta à Rouge
      FastLED.show();
      delay(5);
    }
  }
  // irrecv.resume();
}
void Red()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(243, 2, 2);
  }
  FastLED.show();
}

void Yellow()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(238, 247, 48);
  }
  FastLED.show();
}

void Blue()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(34, 134, 223);
  }
  FastLED.show();
}

void Green()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(32, 223, 23);
  }
  FastLED.show();
}

void Sky()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(59, 222, 251);
  }
  FastLED.show();
}

void Water()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(53, 220, 172);
  }
  FastLED.show();
}

void OrangeF()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(223, 149, 34);
  }
  FastLED.show();
}

void Violetf()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(123, 34, 223);
  }
  FastLED.show();
}

void Pink()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(244, 94, 221);
  }
  FastLED.show();
}

void Eteindre()
{
  for (int i = 0; i < LED_COUNT; i++)
  {
    leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();
}

void setup()
{
  Serial.begin(9600);
  Serial.println("IR Receiver Button Decode");
  irrecv.enableIRIn(); // Start the receiver
  irrecv.blink13(true);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, LED_COUNT);
  FastLED.setBrightness(BRIGHTNESS);
}
void loop()
{
  if (irrecv.decode(&irResults))
  {
    translateIR();

    if (irResults.value == TonsBleus)
    {
      PaletteBlue();
    }
    else if (irResults.value == ChangeDeg)
    {
      changeColor();
    }
    else if (irResults.value == TonsRouges)
    {
      Paletterouge();
    }
    else if (irResults.value == TonsVerts)
    {
      PaletteGreen();
    }
    else if (irResults.value == SwitchOff)
    {
      Eteindre();
    }
    else if (irResults.value == Violet)
    {
      Violetf();
    }
    else if (irResults.value == Rose)
    {
      Pink();
    }
    else if (irResults.value == Rouge)
    {
      Red();
    }
    else if (irResults.value == Orange)
    {
      OrangeF();
    }
    else if (irResults.value == Ciel)
    {
      Sky();
    }
    else if (irResults.value == VertEau)
    {
      Water();
    }
    else if (irResults.value == Bleu)
    {
      Blue();
    }
    else if (irResults.value == Vert)
    {
      Green();
    }
    else if (irResults.value == Jaune)
    {
      Yellow();
    }
    else if (irResults.value == BrightnessP)
    {
      int B = BRIGHTNESS + 50;
      setBrightness(B);
    }
    else if (irResults.value == BrightnessM)
    {
      int B = BRIGHTNESS - 50;
      setBrightness(B);
    }
    // Ajoutez ici des conditions pour les autres boutons de votre télécommande

    irrecv.resume(); // Attente du prochain signal IR
  }
}
