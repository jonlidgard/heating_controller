import wiringpi, logging, time

class Boiler:
    def __init__(self, widget):
        self._pin = 28 
        wiringpi.pinMode(self._pin, 1)
        self._widget = widget
        self._logger = logging.getLogger('heating')
        self._logger.addHandler(logging.NullHandler())
       
        self._run_time = 0

    def set(self, state):
        if (state != 0 and state != 1):
            raise RuntimeError("State not valid binary")
        wiringpi.digitalWrite(self._pin, 1-state)
        self._widget.update(state)

    def on(self):
        if self.get_state() == 0:
            self._logger.info('Boiler: ON')
            self.set(1)
            self._run_time = time.time()

    def off(self):
        if self.get_state() == 1:
            if self._run_time != 0:
                t = (time.time() - self._run_time)
                self._run_time = 0
            else:
                t = 0
            self._logger.info('Boiler: OFF, runtime: %ds',t)
            self.set(0)

    def get_state(self):
        return 1-wiringpi.digitalRead(self._pin)

# Run tests
if __name__ == "__main__":
   import sys, getopt

   wiringpi.wiringPiSetup()
   boiler = Boiler()
#   boiler.off()

   argv = sys.argv[1:]
   opts, args = getopt.getopt(argv,"hm:",["mode="])
   mode=''   
   for opt, arg in opts:
      if opt == '-h':
         print 'boiler.py -m <on/off>'
         sys.exit()
      elif opt in ('-m', 'mode='):
        if arg  == 'on':
            print ('ON')
            boiler.on() 

        elif arg == 'off':
            print ('OFF')
            boiler.off()

