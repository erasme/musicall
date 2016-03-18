#define SIZE 10
const int pins[] = { 12, 11, 10, 8, 6, 7, 3, 4, 5, 13 };
bool values[ SIZE ];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i < SIZE; i++) values[i] = 0;
}

void printValues() {
  for (char i = 0; i < SIZE; i++) {
    Serial.print(values[i]);
    if( i != SIZE - 1 ) Serial.print(":");
  }
  Serial.println();
}

void loop() {
  boolean change = false;
  for (char i = 0; i < SIZE; i++) {
    int capa = readCapacitivePin( pins[ i ] ) > 10;
    if (values[i] != capa ) {
      change = true;
    }
    values[i] = capa;
  }

  if ( change ) {
    printValues();
  }

  delay(20);
}
