import wiringpi

RELAY_PINS = [23,26,9,8]

class Relay:
    def __init__(self, relay_no):
        if (relay_no < 1 or relay_no > len(RELAY_PINS)):
            raise IndexError('Relay out of range')
        self._relay_no = relay_no
        self._pin = RELAY_PINS[self._relay_no-1]
        wiringpi.pinMode(self._pin, 1)

    def set(self, state):
        if (state != 0 and state != 1):
            raise RuntimeError("State not valid binary")
        wiringpi.digitalWrite(self._pin, 1-state)

    def get(self):
        return 1 - wiringpi.digitalRead(self._pin)

    def on(self):
        self.set(1)

    def off(self):
        self.set(0)

    def toggle(self):
        self.set(1-self.get())

print (__name__)

# Run tests
if __name__ == "__main__":
    import time
    wiringpi.wiringPiSetup()

    r1 = Relay(1)
    r2 = Relay(2)
    r3 = Relay(3)
    r4 = Relay(4)
    relays = [r1,r2,r3,r4]

    for i in range(4):
        r = relays[i]
        r.off()

    while True:
        for i in range(4):
            r = relays[i]
            r.toggle()
            time.sleep(.5)
