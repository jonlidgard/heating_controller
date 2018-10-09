from relays import Relay
from bounce import bounce_check
import wiringpi



class ZoneValve:
    def __init__(self, valve_no, notifier):
        self._notifier = notifier
        self._pins = [3,4,5]
        if (valve_no < 1 or valve_no > len(self._pins)):
            raise IndexError('ZoneValve out of range')
        self._valve_no = valve_no
        self._pin = self._pins[self._valve_no-1]
        wiringpi.pinMode(self._pin, 0)
        self._relay = Relay(valve_no)
        self._current_state = "unknown"
        self.check_state()
        self._state_changed = False
        self._debounce = BOUNCE_COUNT
        self._prev_pin_state = -1
    def check_state(self):
        if (self._relay.get() == 1): # Motor on
            if (self.get_limit_switch_state() == 1):
                state = "open"
            else:
                state = "opening"
        else:
            if (self.get_limit_switch_state() == 0):
                state = "closed"
            else:
                state = "closing"
        if (self._current_state != state):
            self._current_state = state
            self._state_changed = True
#        print ('Current State:', self._current_state)
#        print ('State Changed:', self._state_changed)

    def get_channel(self):
        return self._valve_no

    def get_state(self):
        return self._current_state

    def get_limit_switch_state(self):

        pin_state, self._prev_pin_state, self._debounce = \
            bounce_check(self._pin, self._prev_pin_state, self._debounce )
        return pin_state

    def poll(self):
        self.check_state()
        if (self._state_changed == True):
#            print ('Notify')
            self._notifier(self)
            self._state_changed = False

    def open(self):
        self._relay.on()
        self.poll()

    def close(self):
        self._relay.off()
        self.poll()

    def toggle(self):
        self._relay.toggle()
        self.poll()
