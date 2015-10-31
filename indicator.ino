#include <Adafruit_NeoPixel.h>
#include <DigiCDC.h>


Adafruit_NeoPixel strip = Adafruit_NeoPixel(16,1,NEO_GRB | NEO_KHZ800);
# define NONE (255)
unsigned char pos = NONE;
unsigned char colorIndex = 0;
unsigned char color[3];
bool show = false;


void setup() {
  
  SerialUSB.begin();
  strip.begin();
  strip.setBrightness(30);
  
} // setup()


void loop() {

  if (!SerialUSB.available()) {
    if (!show) return;
    SerialUSB.write("okay\n");
    strip.show();
    show = false;
    return;
  }
    
  unsigned char c = SerialUSB.read();
    
  switch (c) {
    case ':': {
      pos = 0;
      colorIndex = 0;
    } break;
    case ';': {
      if (pos > 0) show = true;
      pos = NONE;
      colorIndex = 0;        
    } break;
  } // switch char

  if (pos == NONE) return;
  
  bool isDigit = false;    
  if (('0' <= c) && (c <= '9')) {
    isDigit = true;
    c = c - '0';
  }
  if (('a' <= c) && (c <= 'f')) {
    isDigit = true;
    c = c - ('a' - 10);
  }
  if (('A' <= c) && (c <= 'F')) {
    isDigit = true;
    c = c - ('A' - 10);
  }
  if (!isDigit) return;

  color[colorIndex++] = c | (c << 4);
  if (colorIndex < 3) return;

  strip.setPixelColor(pos,strip.Color(color[0],color[1],color[2]));
  colorIndex = 0;
  pos++;
    
} // loop()
