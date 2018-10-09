/*
 * DigiPotX9Cxxx.cpp - Arduino library for managing digital potentiometers X9Cxxx (xxx = 102,103,104,503).
 * By Timo Fager, Jul 29, 2011.
 * Released to public domain.
 **/

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <iostream>
#include <unistd.h>
using namespace std;

#include <wiringPi.h>
#include "digiPotX9Cxxx.h"


#define constrain(amt,low,high) ((amt)<(low)?(low):((amt)>(high)?(high):(amt)))

int main (int argc, char *argv[])
{ 
// wiringPiSetup () ;
  DigiPot sense_pot(27,0,24);
  DigiPot mode_pot(27,0,28);
  mode_pot.reset();
  sense_pot.reset();
  if (argc > 1) {
    mode_pot.set(atoi(argv[1])); 
    printf("Mode Resistance: %d\n",mode_pot.get());
    sense_pot.set(atoi(argv[2])); 
    printf("Sense Resistance: %d\n", sense_pot.get());
  }
  else {
    for (int i=0; i< 100; i++)
  {
    sleep(1);
    mode_pot.set(i); 
    printf("Mode Resistance: %d\n",mode_pot.get());
  }
  for (int i=0; i< 100; i++)
  {
    sleep(1);
    sense_pot.set(i); 
    printf("Sense Resistance: %d\n", sense_pot.get());
  }
  }
  return 0;
}


DigiPot::DigiPot(uint8_t incPin, uint8_t udPin, uint8_t csPin) {
  _incPin = incPin;
  _udPin = udPin;
  _csPin = csPin;  
  _currentValue = DIGIPOT_UNKNOWN;

  wiringPiSetup () ;
  pinMode(_incPin, OUTPUT);
  pinMode(_udPin, OUTPUT);
  pinMode(_csPin, OUTPUT);
  digitalWrite(_csPin, HIGH);

}

uint8_t DigiPot::reset() {
  // change down maximum number of times to ensure the value is 0
  decrease(DIGIPOT_MAX_AMOUNT);
  _currentValue = 0;
  return _currentValue;
}

 uint8_t DigiPot::set(uint8_t value) {
  value = constrain(value, 0, DIGIPOT_MAX_AMOUNT);
  if (_currentValue == DIGIPOT_UNKNOWN) reset();
  if (_currentValue > value) {
    change(DIGIPOT_DOWN, _currentValue-value);
  } else if (_currentValue < value) {
    change(DIGIPOT_UP, value-_currentValue);
  }
  return _currentValue;
}

uint8_t DigiPot::get() {
  return _currentValue;
}

uint8_t DigiPot::increase(uint8_t amount) {
  amount = constrain(amount, 0, DIGIPOT_MAX_AMOUNT);
  change(DIGIPOT_UP, amount);
  return _currentValue;
}

uint8_t DigiPot::decrease(uint8_t amount) {
  amount = constrain(amount, 0, DIGIPOT_MAX_AMOUNT);
  change(DIGIPOT_DOWN, amount);
  return _currentValue;
}

uint8_t DigiPot::change(uint8_t direction, uint8_t amount) {
  amount = constrain(amount, 0, DIGIPOT_MAX_AMOUNT);
  digitalWrite(_udPin, direction);
  digitalWrite(_incPin, HIGH);
  digitalWrite(_csPin, LOW);

  for (uint8_t i=0; i<amount; i++) {
    digitalWrite(_incPin, LOW);
    delayMicroseconds(2);
    digitalWrite(_incPin, HIGH);
    delayMicroseconds(2);
    if (_currentValue != DIGIPOT_UNKNOWN) {
      _currentValue += (direction == DIGIPOT_UP ? 1 : -1);
      _currentValue = constrain(_currentValue, 0, DIGIPOT_MAX_AMOUNT);
    }
    
  }
  digitalWrite(_csPin, HIGH);
  return _currentValue;
}

extern "C"
{
    DigiPot *DigiPot_new(uint8_t incPin, uint8_t udPin, uint8_t csPin) {
      return new DigiPot(incPin, udPin, csPin);}

    int DigiPot_reset(DigiPot *pot) {return pot->reset();}
    uint8_t DigiPot_get(DigiPot *pot) {return pot->get();}
    uint8_t DigiPot_set(DigiPot *pot, uint8_t n) {return pot->set(n);}
    uint8_t DigiPot_increase(DigiPot *pot, uint8_t n) {return pot->increase(n);}
    uint8_t DigiPot_decrease(DigiPot *pot, uint8_t n) {return pot->decrease(n);}
    uint8_t DigiPot_change(DigiPot *pot, uint8_t d, uint8_t n) {return pot->change(d,n);}
}