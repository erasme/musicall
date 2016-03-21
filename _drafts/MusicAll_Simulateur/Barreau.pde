class Barreau {
    int id;
    int nbZones;
    int[] states;
    int[] lights;

    Barreau(int _id, int _nbZones) {
        id = _id;
        nbZones = _nbZones;
        states = new int[nbZones];
        lights = new int[nbZones];
        for (int i=0; i<nbZones; i++) {
            states[i] = 0;
            lights[i] = 15;
        }
    }

    void draw(int x, int y, int w, int h) {
        pushMatrix();
        translate(x, y);
        float zoneHeight = float(h)/nbZones;
        for (int i=0; i<nbZones; i++) {
            if ( states[i] == 3){
                lights[i] -= 3;
                lights[i] = max( lights[i], 15 );
            }
            
            fill( lights[i] );
            rect(0, zoneHeight*i, w, zoneHeight);
        }
        popMatrix();
    }

    void setState(int i, int value) {
        states[ i ] = value;
        lights[ i ] =  value == 0 ? 15 :
        value == 1 ? 95 :
        value == 2 ? 175 :
        255;
    }
}

