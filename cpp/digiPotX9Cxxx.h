/*
 * DigiPotX9Cxxx.h - Arduino library for managing digital potentiometers X9Cxxx (xxx = 102,103,104,503).
 * By Timo Fager, Jul 29, 2011.
 * Released to public domain.
 **/

#ifndef DigiPotX9Cxxx_h
#define DigiPotX9Cxxx_h

#define DIGIPOT_UP   1
#define DIGIPOT_DOWN 0
#define DIGIPOT_MAX_AMOUNT 99
#define DIGIPOT_UNKNOWN 255
#include <stdint.h>

class DigiPot
{
 public:
  DigiPot(uint8_t incPin, uint8_t udPin, uint8_t csPin);
  uint8_t increase(uint8_t amount);
  uint8_t decrease(uint8_t amount);
  uint8_t change(uint8_t direction, uint8_t amount);
  uint8_t set(uint8_t value);
  uint8_t get();
  uint8_t reset();

 private:
  uint8_t _incPin;
  uint8_t _udPin;
  uint8_t _csPin;
  uint8_t _currentValue;
};

/*
DigiPot *DigiPot_new(uint8_t incPin, uint8_t udPin, uint8_t csPin);

int DigiPot_reset(DigiPot *pot);
uint8_t DigiPot_get(DigiPot *pot);
uint8_t DigiPot_set(DigiPot *pot, uint8_t n);
uint8_t DigiPot_increase(DigiPot *pot, uint8_t n);
uint8_t DigiPot_decrease(DigiPot *pot, uint8_t n);
uint8_t DigiPot_change(DigiPot *pot, uint8_t d, uint8_t n);
*/
#endif
