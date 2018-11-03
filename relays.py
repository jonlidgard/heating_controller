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


# Run tests
if __name__ == "__main__":
    import time
    import sys, getopt
    
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv,"htr:s:",["relay=","state="])
    
    wiringpi.wiringPiSetup()

    r1 = Relay(1)
    r2 = Relay(2)
    r3 = Relay(3)
    r4 = Relay(4)
    relays = [r1,r2,r3,r4]

    for i in range(4):
        r = relays[i]
        r.off()

    relay = -1
    state = -1    
    for opt, arg in opts:
      if opt == '-h':
         print 'relay.py -r <relay> -s <0/1>'
         sys.exit()
      elif opt in ("-r", "--relay"):
         relay = int(arg)-1
      elif opt in ("-s", "--state"):
         state = int(arg)
      elif opt in ("-t"):
         while True:
            for i in range(4):
                r = relays[i]
                r.toggle()
                time.sleep(5)

      if relay > -1:
        if state == 0:
          relays[relay].off() 
        elif state == 1:
          relays[relay].on()
        else:
          relays[relay].toggle()
