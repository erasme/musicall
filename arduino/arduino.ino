#define DIGIPINMAX 5
bool values[ DIGIPINMAX+1 ];
int triggers[ DIGIPINMAX+1 ];
const int RESILIENCE = 7;
const int EXTREM = 45;
const int MAXTRIG = 36;
const int CALIB = 10000;

void setup() {
  
  int peaks[ DIGIPINMAX+1 ];
  long unsigned sums[ DIGIPINMAX+1 ];
  
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i <= DIGIPINMAX; i++) {
    values[i] = 0;
    peaks[i] = 0;
    triggers[i] = 0;
  }
  
  // CALIBRATING
  long count = 0;
  Serial.print("Calibrating... ");
  while( millis() < CALIB) {
    count++;
    for (int i = 2; i <= DIGIPINMAX; i++) {
      int readVal = readCapacitivePin( i );
      if (readVal > peaks[i]) peaks[i] = readVal;
    }
  }
  Serial.println(" done");

  // SHOW PEAKS
  for (int i = 2; i <= DIGIPINMAX; i++) {
    Serial.print(peaks[i]);
    Serial.print(":");
  }
  Serial.println("");

  // CALCULATE TRIGGERS
  for (int i = 2; i <= DIGIPINMAX; i++) {    
    triggers[i] = min(MAXTRIG,(peaks[i]+RESILIENCE));
    Serial.print(triggers[i]);
    Serial.print(":");
  }
  Serial.println("");
  
  Serial.println("Calibrated");
  
  
}


void loop() {
  boolean change = false;
  for (int i = 2; i <= DIGIPINMAX; i++) {
    int readVal = readCapacitivePin( i );
    bool capa =  (readVal >= triggers[i]);
    if (values[i] != capa ) {
      Serial.println("PIN:"+String(i)+":"+String(capa));
      values[i] = capa;
    }
  }

  //delay(10);
}
