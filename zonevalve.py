from relays import Relay
from common import bounce_check
import wiringpi
import logging
import time
import pushover 

LIMIT_PINS = [3,4,5]
ON_TIMEOUT_SECS = 30
OFF_TIMEOUT_SECS = 30

class ZoneValve:
    def __init__(self, valve_no, name, notifier):
        self._name = name
        self._notifier = notifier


        self._logger = logging.getLogger('heating')
        self._logger.addHandler(logging.NullHandler())


        self._pushover_client = pushover.Client("u1nntc8b4zqy9p565krjpnq2wqfp6t", api_token="ayexnq66ykz79gdr8q4wx2tto6qri7")
        
        self.reset_timeout()
        self._valve_timeout = 0
        if (valve_no < 1 or valve_no > len(LIMIT_PINS)):
            raise IndexError('ZoneValve out of range')
        self._valve_no = valve_no
        pin = LIMIT_PINS[valve_no-1] 
        wiringpi.pinMode(pin, 0)
        self._pin_state = {'pin': pin, 'changed': False, 'new': -1, 'stable': -1, 'samples': -1}

        self._relay = Relay(valve_no+1)
        self._valve_state = {'current': 'unknown', 'changed': False}
        self._logger.debug('ZoneValve module started')
        self.check_state()


    def check_state(self):
        motor_on = (self._relay.get() == 1) # Motor on
        switch_made = (self.get_limit_switch_state() == 1)
        now = time.time()
        self._logger.debug('Time now %d',now)
        if motor_on:
            if switch_made:
                state = "open"
                self.reset_timeout()
            else:
                state = "opening"
                self.check_and_warn(ON_TIMEOUT_SECS)
        else:
            if switch_made:
                state = "closing"
                self.check_and_warn(OFF_TIMEOUT_SECS)
            else:
                state = "closed"
                self.reset_timeout()
        
        if (self._valve_state['current'] != state):
            self._valve_state['current'] = state
            self._valve_state['changed'] = True
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('%s valve state changed to %s',self.get_name(), state)
#        print ('Current State:', self._valve_state['current'])
#        print ('State Changed:', self._valve_state['changed'])

    def get_channel(self):
        return self._valve_no


    def get_name(self):
        return self._name

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
        self.set_timeout(ON_TIMEOUT_SECS)
        self._logger.debug('Time valve open cmd %d',self._valve_timeout)
        self._relay.on()
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('%s Motor Relay ON',self.get_name())
        self.poll()

    def close(self):
        self.set_timeout(OFF_TIMEOUT_SECS)
        self._logger.debug('Time valve close cmd %d',self._valve_timeout)
        self._relay.off()
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('%s Motor Relay OFF',self.get_name())
        self.poll()

    def toggle(self):
        self._relay.toggle()
        self.poll()

    def timed_out(self):
        return self._valve_timeout != 0 and self._valve_timeout < time.time()

    def reset_timeout(self):
        self._valve_timeout = 0

    def set_timeout(self, secs):
        self._valve_timeout = time.time() + secs 

    def check_and_warn(self, secs):
        if self.timed_out():
            msg = '{} valve failed to open in {}s'.format(self.get_name(),secs)
            self._logger.warn(msg)
            self._pushover_client.send_message(msg, title="Warning")
            self._valve_timeout = 0


# Tests

def printState(valve):
    state = (valve.get_state())
    print ('Valve:', valve.get_channel(), valve.get_name(), '-', state)
    if (state == "open" or state == "closed"):
        valve.toggle()


if __name__ == "__main__":
    import time

    msg = '{} valve failed to open in {}s'.format('test',10)
    print (msg)
    wiringpi.wiringPiSetup()
    zv1 = ZoneValve(1, 'ufh', printState)
    zv2 = ZoneValve(2, 'downstairs', printState)
    zv3 = ZoneValve(3, 'upstairs', printState)
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
