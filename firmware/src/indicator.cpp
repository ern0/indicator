#include <Adafruit_NeoPixel.h>
#include "indicator.hpp"

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXELS, PIN_NEOPIX, NEO_GRB | NEO_KHZ800);

unsigned char pos = POS_NONE;
unsigned char colorIndex = 0;
unsigned char color[3];
bool posReset = true;
unsigned char brite = 30;
unsigned char mod = MOD_IDLE;
unsigned char c;


void setup() {

	Serial.begin(9600);
	strip.begin();
	strip.setBrightness(30);

	clear(0xff,0xff,0xff);

} // setup()


void loop() {

	c = Serial.read();

	procChar();
	procMode();

} // loop()


bool procChar() {

	switch (c) {

		case '!':
			clear(0,0,0);
			return true;

		case '?':
			Serial.write(SIGNATURE);
			return true;

		case '*':
			mod = MOD_BRITE;
			brite = 0;
			pos = POS_NONE;
			posReset = true;
			break;

		case '+':
			mod = MOD_POS;
			pos = POS_NONE;
			posReset = false;
			break;

		case ':':
			mod = MOD_DATA;
			if (posReset) pos = 0;
			colorIndex = 0;
			break;

		case ';':
			mod = MOD_IDLE;
			bool show = ( pos > 0 );
			if (pos == POS_NONE) show = false;
			if (show) strip.show();
			pos = POS_NONE;
			colorIndex = 0;
			posReset = true;
			break;

	} // switch char

	return false;
} // procChar()


void procMode() {

	switch (mod) {

		case MOD_DATA:

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

			break;

		case MOD_POS:

			if ((c < '0') || ('9' < c)) return;
			if (pos == POS_NONE) pos = 0;

			pos = 10 * pos;
			pos += (c - '0');

			break;

		case MOD_BRITE:

			if ((c < '0') || ('9' < c)) return;

			brite = 10 * brite;
			brite += (c - '0');

			break;

	} // switch mod

} // procMode()


void clear(int r,int g,int b) {

	for (int n = 0; n < PIXELS; n++) strip.setPixelColor(n,r,g,b);
	strip.show();

	pos = POS_NONE;

} // clear()
