# Indicator

## Ezmiez

### Cél

A projekt célja, hogy segítse a WS2812-t használó RGB ledes installációk gyors elkészítését.

### Követelmények

A firmware Arduino kompatibilis eszközökre készült, amelyhez az egyik digital out lábon WS2812 led lánc van kötve.

Tesztelt rendszerek:
 - Arduino Uno/Nano (Atmel 328)
 - Digispark ATTiny85

Az eszközt USB-n lehet a hostra kötni, Linuxon nem kell hozzá külön driver.

## Használat

### Fordítási paraméterek

A pixelek számának csak ott van jelentősége, hogy az e fölötti pixelekre vonatkozó parancsokat az eszköz lenyeli.
```
# define PIXELS 40
```

Fordítási paraméterként kell megadni azon digital out pin számát, amelyekre a ledek kötve vannak.
```
# define PIN 13
```

### Indulás

Bekapcsoláskor vagy resetkor az eszköz rövid ideig
felvillantja az összes (ld. `PIXELS` fordítási paraméter) led-et sötétkék színnel.

### Serial

Az eszköz soros paraméterei: 9600,n,8,1.

Az eszköz az alábbi portokon szokott megjelenni:
- Linux: `/dev/ttyUSB0` vagy `/dev/ttyACM0`
- Mac OS: `/dev/tty.wchusbserial1410`

**Figyelem!** Az eszköz host csatlakozása után resetel, az első parancs kiadása előtt célszerű kb. 1 másodpercet várni! (A csatlakozáskori reset [kiküszöbölhető egy ellenállás beiktatásával](http://playground.arduino.cc/Main/DisablingAutoResetOnSerialConnection).)

### Parancsok

Az eszköz parancsai karakteres formátumúak, így akár serial terminálból is ki lehet adni őket. Több parancsot egy sorba is lehet írni (kivéve a *sötétség* parancsot).

#### Fényerő: `*` (csillag)

A ledek láthatósága a fényviszonyoktól függ. Ezzel a paranccsal egy általános világosság adható meg. Kezdetnek alacsony értékeket adjunk meg, a WS2812 nagyon fényes.

Példa: `*30` - szobai körülményekhez megfelelő érték. 

A parancs a pozíciót 0-ra állítja (lásd *pozíció* parancs).

A parancs a már kigyújtott ledek fényerejét nem változtatja meg, így célszerű a csatlakozáskor azonnal, egyszer kiküldeni.

#### Pozíció: `+` (plusz)

Megadja a következő vezérelni kívánt led számát. Ennek alapértéke 0, így ha nem küldünk ki *pozíció* parancsot, a *szín* parancsok az első ledtől kezdve érvényesek.

Példa: 12. led elsötétítése: `+12:000;`

A *fényerő* és a *vége* parancs a pozíciót nullára állítja.

#### Szín: `:` (kettőspont)

Az aktuális ledhez színt rendel. A színt 3-jegyű hexadecimális számmal kell megadni (kis- vagy nagybetű használata egyaránt megengedett).

Példa: 8. led kékre állítása: `+8:0F0;`

A paranccsal több led értékét is meg lehet adni, elég az RGB értékeket egymás mögé írni. Az olvashatóság kedvéért `-` (mínusz) jel írható az egyes értékek közé.

Példa: 4 led lekapcsolása: `:000-000-000-000;`

#### Kiküldés: `;` (pontosvessző)

A *szín* paranccsal megadott értékek csak ennek a parancsnak a hatására lépnek érvénybe. A parancs a pozíció számlálót 0-ra állítja.

Példa: 8. és 12. led fehérre állítása: `+8:fff+12:fff;`

#### Sötétség: `!` (felkiáltójel)

Ez a parancs azonnal kikapcsolja az összes ledet, nem kell *kiküldés* parancs sem utána. A fényerőt nem változtatja meg, viszont a pozíciót nullára állítja.
