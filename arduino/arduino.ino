#define DIGIPINMAX 50
bool values[ DIGIPINMAX+1 ];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i <= DIGIPINMAX; i++) values[i] = 0;
  //Serial.println("HELLO");
}

void printValues() {
  for (int i = 0; i <= DIGIPINMAX; i++) {
    Serial.print(values[i]);
    if( i != DIGIPINMAX ) Serial.print(":");
  }
  Serial.println();
}

void loop() {
  boolean change = false;
  for (int i = 2; i <= DIGIPINMAX; i++) {
    int readVal = readCapacitivePin( i );
    bool capa =  readVal > 4;
    if (values[i] != capa ) {
      //change = true;
      Serial.println("PIN:"+String(i)+":"+String(capa));
      values[i] = capa;
    }
  }

  if ( change ) {
    printValues();
  }

  //delay(10);
}
