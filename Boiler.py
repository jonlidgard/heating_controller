from digiPotX9C import DigiPot

mode_fixed_resistance = 5600
temp_fixed_resistance = 0
SETPOINT_TEMP_MAX = 30.0
SETPOINT_RESISTANCE_MAX = 2200
POT_FACTOR = 1000
MODES = {'night': 13960, 'frost': 12650, 'comfort': 8960, 'scheduled': 6220}

class Boiler:
    def __init__(self):
        self.temp_pot = DigiPot(27,0,24)
        self.mode_pot = DigiPot(27,0,28)
        self.reset()
        
    def temp_to_resistance(self,t):
        t = (SETPOINT_TEMP_MAX - t) / SETPOINT_TEMP_MAX
        return int(t * SETPOINT_RESISTANCE_MAX)

    def resistance_to_steps(self, fixed_r, r):
        return int((r - fixed_r) / POT_FACTOR)

    def set_temp(self, r):
        steps = self.resistance_to_steps(temp_fixed_resistance, r)
        print (steps)
        self.temp_pot.set(steps)

    def set_mode(self, mode, setpoint):
	print (mode,setpoint)
        r = MODES[mode]
        
        print(r)
        if mode == "comfort" or mode == 'scheduled':
          r += self.temp_to_resistance(setpoint)    
        steps = self.resistance_to_steps(mode_fixed_resistance, r)

	print (r, steps)
        self.mode_pot.set(steps)

    def reset(self):
        self.temp_pot.reset()
        self.mode_pot.reset()

    def on(self):
        self.set_mode('comfort',20)

    def off(self):
        self.set_mode('comfort',5)

# Run tests
if __name__ == "__main__":
   import wiringpi, sys, getopt

   wiringpi.wiringPiSetup()
   boiler = Boiler()
   boiler.reset()

   argv = sys.argv[1:]
   opts, args = getopt.getopt(argv,"hm:s:t:",["mode=","setpoint=","temp="])
   mode=''   
   setpoint=-1
   temp=-1    
   for opt, arg in opts:
      if opt == '-h':
         print 'boiler.py -m <mode> -s <setpoint> -t <temp>'
         sys.exit()
      elif opt in ("-m", "--mode"):
        if arg  == 'on':
          boiler.on() 
        elif arg == 'off':
          boiler.off()
        else:
          mode = arg
      elif opt in ("-s", "--setpoint"):
         setpoint = int(arg)
      elif opt in ("-t", "--temp"):
         temp = int(arg)
   if mode != '' and setpoint>-1:
     boiler.set_mode(mode, setpoint)
   if temp>-1:
     boiler.set_temp(temp)

