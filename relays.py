import wiringpi


class Relay:
    def __init__(self, relay_no):
        self._pins = [23,26,9,8]
        if (relay_no < 1 or relay_no > len(self._pins)):
            raise IndexError('Relay out of range')
        self._relay_no = relay_no
        self._pin = self._pins[self._relay_no-1]
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
