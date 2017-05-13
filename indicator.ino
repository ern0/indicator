#include <Adafruit_NeoPixel.h>
///#include <DigiCDC.h>

# define PIXELS 128
# define PIN 13

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXELS, PIN, NEO_GRB | NEO_KHZ800);
# define POS_NONE (255)
unsigned char pos = POS_NONE;
unsigned char colorIndex = 0;
unsigned char color[3];
bool posReset = true;
unsigned char brite = 30;

# define MOD_IDLE (0)
# define MOD_BRITE (1)
# define MOD_POS (2)
# define MOD_DATA (3)
unsigned char mod = MOD_IDLE;


void setup() {

  Serial.begin(38400);
  strip.begin();
  strip.setBrightness(30);

  for (int n = 0; n < PIXELS; n++) strip.setPixelColor(n,0,0,11);
  strip.show();
  delay(500);
  for (int n = 0; n < PIXELS; n++) strip.setPixelColor(n,0,0,0);
  strip.show();

} // setup()


void loop() {

  unsigned char c = Serial.read();

  switch (c) {

    case '*': {
        mod = MOD_BRITE;
        brite = 0;
        pos = POS_NONE;
        posReset = true;
      } break;

    case '+': {
        mod = MOD_POS;
        pos = POS_NONE;
        posReset = false;
      } break;

    case ':': {
        mod = MOD_DATA;
        if (posReset) pos = 0;
        colorIndex = 0;
      } break;

    case ';': {
        mod = MOD_IDLE;
        bool show = ( pos > 0 );
        if (pos == POS_NONE) show = false;
        if (show) strip.show();
        pos = POS_NONE;
        colorIndex = 0;
        posReset = true;
      } break;

  } // switch char

  switch (mod) {

    case MOD_DATA: {
        //if (pos == POS_NONE) return;
        if (pos >= PIXELS) return;

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

        if (brite == 0) brite = 30;
        strip.setBrightness(brite);
        strip.setPixelColor(pos, color[0], color[1], color[2]);
        colorIndex = 0;
        pos++;

      } break;

    case MOD_POS: {

        if ((c < '0') || ('9' < c)) return;
        if (pos == POS_NONE) pos = 0;

        pos = 10 * pos;
        pos += (c - '0');

      } break;

    case MOD_BRITE: {

        if ((c < '0') || ('9' < c)) return;

        brite = 10 * brite;
        brite += (c - '0');

      } break;

  } // switch mod

} // loop()
