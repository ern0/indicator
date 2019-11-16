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

struct {
	int pin;
	int pressed;
	int last;
} button[2];


void setup() {

	pinMode(PIN_GND1,OUTPUT);
	digitalWrite(PIN_GND1,LOW);
	pinMode(PIN_BUTTON1,INPUT);
	button[0].pin = PIN_BUTTON1;
	button[0].pressed = 0;

	pinMode(PIN_GND2,OUTPUT);
	//digitalWrite(PIN_GND2,HIGH);
	pinMode(PIN_BUTTON2,INPUT_PULLUP);
	button[1].pin = PIN_BUTTON2;
	button[1].pressed = 0;

	for (int i = 0; i < BUTTONS; i++) button[i].last = -1;

	Serial.begin(9600);

	strip.begin();
	strip.setBrightness(30);
	clear(0xff,0xff,0xff);

} // setup()


void loop() {

	while (Serial.available() > 0) {
		c = Serial.read();
		if ( procChar() ) break;
		procMode();
		break;
	}

	for (int i = 0; i < BUTTONS; i++) procInputs(i);

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
	bool isDigit;

	switch (mod) {

		case MOD_DATA:

			if (pos >= PIXELS) return;

			isDigit = false;
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


void procInputs(int i) {

	int actual = ( digitalRead(button[i].pin) == button[i].pressed );

	if (actual == button[i].last) return;
	button[i].last = actual;

	if (actual)	Serial.print(i+1);
	delay(50);

} // procInputs()
