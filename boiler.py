from DigiPotX9C import DigiPot

mode_fixed_resistance = 5600
temp_fixed_resistance = 0
SETPOINT_TEMP_MAX = 30.0
SETPOINT_RESISTANCE_MAX = 2200
POT_FACTOR = 1000
modes = {'night': 13960, 'frost': 12650, 'comfort': 8960, 'scheduled': 6220}

class Boiler:
    def __init__(self):
        self.temp_pot = DigiPot(27,0,24)
        self.mode_pot = DigiPot(27,0,28)
    
    def temp_to_resistance(self,t):
        t = (SETPOINT_TEMP_MAX - t) / SETPOINT_TEMP_MAX
        return t * SETPOINT_RESISTANCE_MAX

    def resistance_to_steps(self, fixed_r, r):
        return (r - fixed_r) / POT_FACTOR

    def set_temp(self, r):
        steps = self.resistance_to_steps(temp_fixed_resistance, r)
        self.temp_pot.set(steps)

    def set_mode(self, mode, setpoint):
        r = modes{mode}
        if mode == "comfort" or mode == 'scheduled':
            r += self.temp_to_resistance(setpoint)    
        steps = self.resistance_to_steps(mode_fixed_resistance, r)
        self.mode_pot.set(steps)

    def reset(self):
        self.temp_pot.reset()
        self.mode_pot.set()
