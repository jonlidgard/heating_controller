from digiPotX9C import DigiPot
import time

mode_fixed_resistance = 5600
temp_fixed_resistance = 0
SETPOINT_TEMP_MAX = 30.0
SETPOINT_RESISTANCE_MAX = 2200
POT1_FACTOR = 1000
POT2_FACTOR = 100
MODES = {'night': 13960, 'frost': 12650, 'comfort': 8960, 'scheduled': 6220}

temp_pot = DigiPot(27,0,24)
mode_pot = DigiPot(27,0,28)
temp_pot.reset()
mode_pot.reset()

for i in range(100):
  print(5590+i*100)
  mode_pot.increase(1)
  temp_pot.increase(1)
  time.sleep(2)
