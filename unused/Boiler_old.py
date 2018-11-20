from digiPotX9C import DigiPot

mode_fixed_resistance = 5590
temp_fixed_resistance = 0
SETPOINT_TEMP_MAX = 30.0
SETPOINT_RESISTANCE_MAX = 2200
POT1_FACTOR = 1000
POT2_FACTOR =  100
MODES = {'night': 13960, 'frost': 12650, 'comfort': 8960, 'scheduled': 6220}

class Boiler:
    def __init__(self):
        self.temp_pot = DigiPot(27,0,24)
        self.mode_pot = DigiPot(27,0,28)
        self.reset()

    def temp_to_resistance(self,t):
        t = (SETPOINT_TEMP_MAX - t) / SETPOINT_TEMP_MAX
        return int(round((t * SETPOINT_RESISTANCE_MAX),0))

    def resistance_to_steps(self, fixed_r, pf, r):
        print fixed_r, pf, r
        res = r - fixed_r
        print res
        s = int(round((res / pf),0))
        print s
        return s

    def set_temp(self, r):
        steps = self.resistance_to_steps(temp_fixed_resistance, POT1_FACTOR, r)
        print (steps)
        self.temp_pot.set(steps)

    def set_mode(self, mode, setpoint):
	print (mode,setpoint)
        r = MODES[mode]
        
        if mode == "comfort" or mode == 'scheduled':
          r += self.temp_to_resistance(setpoint)    
        steps = self.resistance_to_steps(mode_fixed_resistance, POT2_FACTOR, r)

	print (r, steps)
        self.mode_pot.set(steps)

    def reset(self):
        self.temp_pot.reset()
        self.mode_pot.reset()

    def on(self):
        self.mode_pot.set(95)
        #self.set_mode('comfort',20)

    def off(self):
        self.mode_pot.set(5)
        # self.set_mode('comfort',5)

    def step(self, steps):
        self.mode_pot.set(steps)
# Run tests
if __name__ == "__main__":
   import wiringpi, sys, getopt

   wiringpi.wiringPiSetup()
   boiler = Boiler()
   boiler.reset()

   argv = sys.argv[1:]
   opts, args = getopt.getopt(argv,"hm:s:t:x:",["mode=","setpoint=","temp="])
   mode=''   
   setpoint=-1
   temp=-1    
   for opt, arg in opts:
      if opt == '-h':
         print 'boiler.py -m <mode> -s <setpoint> -t <temp>'
         sys.exit()
      elif opt in ('-m', 'mode='):
        if arg  == 'on':
            print 'Boiler: ON'
            boiler.on() 
        elif arg == 'off':
            print 'Boiler: OFF'
            boiler.off()
        else:
            print 'Boiler: Mode'
            mode = arg
      elif opt in ("-s", "--setpoint"):
         print 'Boiler: Setpoint'
         setpoint = int(arg)
      elif opt in ("-t", "--temp"):
         temp = int(arg)
      elif opt in ("-x", "--temp"):
         boiler.step(int(arg))
   if mode != '' and (mode in ('night', 'frost') or setpoint>-1):
     print 'Boiler: Mode Setpioint'
     boiler.set_mode(mode, setpoint)
   if temp>-1:
     boiler.set_temp(temp)

