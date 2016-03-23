#define DIGIPINMAX 50
int means[ DIGIPINMAX+1 ];
bool values[ DIGIPINMAX+1 ];
int triggers[ DIGIPINMAX+1 ];
const int RESILIENCELOW = -5;  //For High Values
const int RESILIENCEMID = -2;  //For Mid values
const int RESILIENCEHIGH = 5;  //For Low values
const int EXTREM = 65;
int MAXTRIG = EXTREM-8;
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
    if (peaks[i]<(EXTREM/3)) 
      triggers[i] = min(MAXTRIG,(peaks[i]+RESILIENCEHIGH));
    else if (peaks[i]<(2*EXTREM/3)) 
      triggers[i] = min(MAXTRIG,(peaks[i]+RESILIENCEMID));
    else
      triggers[i] = min(MAXTRIG,(peaks[i]+RESILIENCELOW));
    Serial.print(triggers[i]);
    Serial.print(":");
  }
  Serial.println("");
  
  Serial.println("Calibrated");
  
  
}


void loop() {

  for (int i = 2; i <= DIGIPINMAX; i++) means[i] = 0;

  int Nround = 4;
  for (int rnd=0; rnd < Nround; rnd++)
    for (int i = 2; i <= DIGIPINMAX; i++)
      means[i] += readCapacitivePin( i );
    
  for (int i = 2; i <= DIGIPINMAX; i++)
      means[i] = means[i]/4;

  for (int i = 2; i <= DIGIPINMAX; i++) {
    bool capa =  (means[i] >= triggers[i]);
    if (values[i] != capa ) {
      Serial.println("PIN:"+String(i)+":"+String(capa)+":"+String(triggers[i]));
      values[i] = capa;
    }
  }
  
  

  //delay(10);
}
