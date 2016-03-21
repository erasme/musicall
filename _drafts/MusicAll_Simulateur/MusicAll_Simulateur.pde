import processing.serial.*;
Serial port;

int nbBar = 5;
int nbZones = 2;
Barreau[] bars;
int margeX = 40;
int count, currentBar, nextBar, currentZone, nextZone;

void setup() {
    size(800, 400);

    printArray(Serial.list());
    port = new Serial(this, "COM6", 9600);

    noStroke();
    bars = new Barreau[nbBar];
    for (int i=0; i<nbBar; i++) {
        bars[i] = new Barreau(i, nbZones);
    }

    setNextZones();
}

void readPort() {
    while ( port.available () > 0 ) {
        String data = port.readStringUntil( '\n' );
        if ( data != null ) {
            if (data.indexOf("1") != -1) {

                String[] tmp = splitTokens(data, ":");
                println( tmp );
                if ( tmp[ currentBar * nbZones + currentZone ].equals( "1" ) ) {
                    bars[ currentBar ].setState( currentZone, 3 );
                    println( "good note" );
                } else {
                    println( "bad note" );
                    bars[ currentBar ].setState( currentZone, 0 );
                }

                count++;
                setNextZones();
            }
        }
    }
}

void setNextZones() {
    currentZone = int(noise(count/2.)*nbZones);
    nextZone = int(noise((count+1)/2.)*nbZones);
    currentBar = count % nbBar;
    bars[currentBar].setState(currentZone, 2);
    nextBar = currentBar + 1;
    if (nextBar < nbBar ) bars[nextBar].setState(nextZone, 1);
    println(currentBar, currentZone);
}

void draw() {
    readPort();

    background(0);

    for (int i=0; i<nbBar; i++) {
        bars[i].draw(margeX + (width-margeX)/nbBar*i - 5, 40, 10, height - 80 );
    }
}

