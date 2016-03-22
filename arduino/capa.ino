// readCapacitivePin
// Input: Arduino pin number
// Output: A number, from 0 to 17 expressing
// how much capacitance is on the pin
// When you touch the pin, or whatever you have
// attached to it, the number will get higher
//#include "pins_arduino.h" // Arduino pre-1.0 needs this
uint8_t readCapacitivePin(int pinToMeasure) {
  // Variables used to translate from Arduino to AVR pin naming
  volatile uint8_t* port;
  volatile uint8_t* ddr;
  volatile uint8_t* pin;
  // Here we translate the input pin number from
  // Arduino pin number to the AVR PORT, PIN, DDR,
  // and which bit of those registers we care about.
  byte bitmask;
  port = portOutputRegister(digitalPinToPort(pinToMeasure));
  ddr = portModeRegister(digitalPinToPort(pinToMeasure));
  bitmask = digitalPinToBitMask(pinToMeasure);
  pin = portInputRegister(digitalPinToPort(pinToMeasure));
  // Discharge the pin first by setting it low and output
  *port &= ~(bitmask);
  *ddr |= bitmask;
  delay(1);
  uint8_t SREG_old = SREG; //back up the AVR Status Register
  // Prevent the timer IRQ from disturbing our measurement
  noInterrupts();
  // Make the pin an input with the internal pull-up on
  *ddr &= ~(bitmask);
  *port |= bitmask;
  // Now see how long the pin to get pulled up. This manual unrolling of the loop
  // decreases the number of hardware cycles between each read of the pin,
  // thus increasing sensitivity.
  uint8_t cycles = 45;
  if (*pin & bitmask) {
    cycles = 0;
  }
  else if (*pin & bitmask) {
    cycles = 1;
  }
  else if (*pin & bitmask) {
    cycles = 2;
  }
  else if (*pin & bitmask) {
    cycles = 3;
  }
  else if (*pin & bitmask) {
    cycles = 4;
  }
  else if (*pin & bitmask) {
    cycles = 5;
  }
  else if (*pin & bitmask) {
    cycles = 6;
  }
  else if (*pin & bitmask) {
    cycles = 7;
  }
  else if (*pin & bitmask) {
    cycles = 8;
  }
  else if (*pin & bitmask) {
    cycles = 9;
  }
  else if (*pin & bitmask) {
    cycles = 10;
  }
  else if (*pin & bitmask) {
    cycles = 11;
  }
  else if (*pin & bitmask) {
    cycles = 12;
  }
  else if (*pin & bitmask) {
    cycles = 13;
  }
  else if (*pin & bitmask) {
    cycles = 14;
  }
  else if (*pin & bitmask) {
    cycles = 15;
  }
  else if (*pin & bitmask) {
    cycles = 16;
  }
  else if (*pin & bitmask) {
    cycles = 17;
  }
  else if (*pin & bitmask) {
    cycles = 18;
  }
  else if (*pin & bitmask) {
    cycles = 19;
  }
  else if (*pin & bitmask) {
    cycles = 20;
  }
  else if (*pin & bitmask) {
    cycles = 21;
  }
  else if (*pin & bitmask) {
    cycles = 22;
  }
  else if (*pin & bitmask) {
    cycles = 23;
  }
  else if (*pin & bitmask) {
    cycles = 24;
  }
  else if (*pin & bitmask) {
    cycles = 25;
  }
  else if (*pin & bitmask) {
    cycles = 26;
  }
  else if (*pin & bitmask) {
    cycles = 27;
  }
  else if (*pin & bitmask) {
    cycles = 28;
  }
  else if (*pin & bitmask) {
    cycles = 29;
  }
  else if (*pin & bitmask) {
    cycles = 30;
  }
  else if (*pin & bitmask) {
    cycles = 31;
  }
  else if (*pin & bitmask) {
    cycles = 32;
  }
  else if (*pin & bitmask) {
    cycles = 33;
  }
  else if (*pin & bitmask) {
    cycles = 34;
  }
  else if (*pin & bitmask) {
    cycles = 35;
  }
  else if (*pin & bitmask) {
    cycles = 36;
  }
  else if (*pin & bitmask) {
    cycles = 37;
  }
  else if (*pin & bitmask) {
    cycles = 38;
  }
  else if (*pin & bitmask) {
    cycles = 39;
  }
  else if (*pin & bitmask) {
    cycles = 40;
  }
  else if (*pin & bitmask) {
    cycles = 41;
  }
  else if (*pin & bitmask) {
    cycles = 42;
  }
  else if (*pin & bitmask) {
    cycles = 43;
  }
  else if (*pin & bitmask) {
    cycles = 44;
  }
  // End of timing-critical section; turn interrupts back on if they were on before, or leave them off if they were off before
  SREG = SREG_old;
  // Discharge the pin again by setting it low and output
  // It's important to leave the pins low if you want to
  // be able to touch more than 1 sensor at a time - if
  // the sensor is left pulled high, when you touch
  // two sensors, your body will transfer the charge between
  // sensors.
  *port &= ~(bitmask);
  *ddr |= bitmask;
  return cycles;
}
