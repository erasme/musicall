
const int SIZE = 3;
bool values[SIZE];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i< SIZE; i++) values[i] = 0;
}

void printpin(int pin) {
  Serial.print(readCapacitivePin(pin));
  Serial.print("/");
}

void loop() {

  bool dirty = false;
  for (int i = 0; i< SIZE; i++) {
    bool val = (readCapacitivePin(6+i) > 10);
    if (values[i] != val) {
      values[i] = val;
      dirty = true;
    }
  }
  if (dirty) {
    for (int i = 0; i< SIZE; i++) {
      Serial.print(values[i]);
      Serial.print("/");
    }
    Serial.println("$");
  }
 
  delay(50);
  
  //Serial.print("\t");
  //Serial.println(readCapacitivePin(7));

  /*if (value0 > 10) tone(9, 300, 10);
  else if (value1 > 10) tone(9, 600, 10);
  else if (value2 > 10) tone(9, 1000, 10);
  else tone(9, 0, 10);
  */
}
