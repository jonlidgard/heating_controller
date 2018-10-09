from relays import Relay
from common import bounce_check
import wiringpi

LIMIT_PINS = [3,4,5]


class ZoneValve:
    def __init__(self, valve_no, notifier):
        self._notifier = notifier
        if (valve_no < 1 or valve_no > len(LIMIT_PINS)):
            raise IndexError('ZoneValve out of range')
        self._valve_no = valve_no
        pin = LIMIT_PINS[valve_no-1] 
        wiringpi.pinMode(pin, 0)
        self._pin_state = {'pin': pin, 'old': -1, 'new': -1, 'stable': -1, 'samples': -1}

        self._relay = Relay(valve_no)
        self._valve_state = {'current': 'unknown', 'changed': False}
        self.check_state()

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
        if (self._valve_state['current'] != state):
            self._valve_state['current'] = state
            self._valve_state['changed'] = True
#        print ('Current State:', self._valve_state['current'])
#        print ('State Changed:', self._valve_state['changed'])

    def get_channel(self):
        return self._valve_no

    def get_state(self):
        return self._valve_state['current']

    def get_limit_switch_state(self):
        # get the new pin state
        self._pin_state['new'] = 1-wiringpi.digitalRead(self._pin_state['pin'])
        self._pin_state = bounce_check(self._pin_state)

        return self._pin_state['stable']

    def poll(self):
        self.check_state()
        if (self._valve_state['changed'] == True):
#            print ('Notify')
            self._notifier(self)
            self._valve_state['changed'] = False

    def open(self):
        self._relay.on()
        self.poll()

    def close(self):
        self._relay.off()
        self.poll()

    def toggle(self):
        self._relay.toggle()
        self.poll()



# Tests

def printState(valve):
    state = (valve.get_state())
    print ('Valve:', valve.get_channel(), '-', state)
    if (state == "open" or state == "closed"):
        valve.toggle()


if __name__ == "__main__":
    import time

    wiringpi.wiringPiSetup()
    zv1 = ZoneValve(1, printState)
    zv2 = ZoneValve(2, printState)
    zv3 = ZoneValve(3, printState)
    valves = [zv1,zv2,zv3]

    for v in valves:
        v.close()
    time.sleep(2)
    for v in valves:
        v.open()
    time.sleep(2)

    while True:
        for v in valves:
            v.poll()
        time.sleep(.5)
